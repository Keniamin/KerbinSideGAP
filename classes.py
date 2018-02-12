import re
from random import randint
from itertools import chain

import utils
import geometry
from beacons import BEACONS

ICONS_PATH = 'ContractPacks/KerbinSideGAP/Icons/'
DEFAULT_AGENT = 'Kerbin Side GAP'


# ===== Basic classes ===== #

class LocationAltitude(object):
    """
    Class to simplify conversions between relative (above ground)
    and absolute (above sea level) altitudes.
    """

    def __init__(self, relative, ground):
        """
        @param relative Altitude above the ground.
        @param ground Altitude of the ground above sea level.
        """
        self.relative = relative
        self.ground = ground

    @property
    def absolute(self):
        return self.ground + self.relative

    def __str__(self):
        return '<Altitude "{}+{}">'.format(self.ground, self.relative)


class Location(object):
    """Totally describes separate location at Kerbin."""

    def __init__(
        self, name, description,
        helipad=None,
        aircraft_launch=None,
        aircraft_parking=None,
        staff_spawn=None, vip_spawn=None,
        launch_refund=None, recovery_factor=None,
        kk_base_name=None,
        runways=None,
        aircraft_launch_allowed_distance=20,
    ):
        """
        @param name Short name of the location.
        @param description Full description of the location.
        @param helipad Point where craft spawns when the player selects
                       location's helipad as a launch site.
        @param aircraft_launch Point where craft spawns when the player selects
                               location's runway as a launch site.
        @param aircraft_parking Point at which aircraft must be parked to
                                complete the contract (helipad would be another
                                one, if available). By default equals to the
                                aircraft_launch. Useful if you want to move
                                marker to the part of the base which looks like
                                a better place for parking (for example, at the
                                KSC it may be a concrete pad between the runway
                                and the Space Plane Hangar).
        @param staff_spawn Point around which staff Kerbals would appear for
                           the service contracts from this location (if any).
        @param vip_spawn Point at which VIP Kerbal would appear for the
                         business flight contracts from this location (if any).
        @param launch_refund Percent of launch cost that player gets on launch.
                             By default equals to 0.
        @param recovery_factor Percent of aircraft cost that player gets on
                               recovery by this base. By default equals to 50.
        @param kk_base_name Name of the launch site in the original .cfg file
                            for checking the base existence using KKCCExt. By
                            default equals to name.
        @param runways List of location's runways. Each runway is described by
                       a pair of it's endpoints. Endpoint is 4-tuple containing
                       latitude, longitude, altitude (above sea level) and
                       minimal glide slope angle required to go safely above
                       obstacles while landing at this endpoint (or None, which
                       means deny such landings absolutely). First endpoint of
                       the first runway must corresponds aircraft_launch point.
        @param aircraft_launch_allowed_distance Tolerance distance for launching
                                              an aircraft from the runway (the
                                              only meaningful use is KSC, that
                                              have different aircraft_launch
                                              points for different runway
                                              upgrade levels).
        """
        self.name = name
        self.description = description
        self.helipad = helipad
        self.aircraft_launch = aircraft_launch
        self.aircraft_parking = aircraft_parking
        self.staff_spawn = staff_spawn
        self.vip_spawn = vip_spawn
        self.launch_refund = launch_refund
        self.recovery_factor = recovery_factor
        self.kk_base_name = kk_base_name
        self.runways = runways
        self.aircraft_launch_allowed_distance = aircraft_launch_allowed_distance
        if self.launch_refund is None:
            self.launch_refund = 0
        if self.recovery_factor is None:
            self.recovery_factor = 50
        if self.aircraft_parking is None:
            self.aircraft_parking = self.aircraft_launch
        if self.kk_base_name is None:
            self.kk_base_name = self.name
        if self.aircraft_launch is not None and self.runways is not None:
            dist = geometry.distance(self.aircraft_launch, self.runways[0][0])
            assert dist == min(
                geometry.distance(self.aircraft_launch, pt)
                for pt in chain.from_iterable(self.runways)
            ), 'Mismatch aircraft_launch and runways for {}'.format(self.name)

    @property
    def position(self):
        return self.helipad or self.aircraft_launch

    @property
    def alphanum_name(self):
        return re.sub(r'[^a-zA-Z0-9]', '', self.name)

    def __str__(self):
        return '<Location "{}">'.format(self.name)


class Contract(object):
    """Base class for all Kerbin Side GAP contract types."""
    route_color = 'black' # default color of the route on the map
    max_simultaneous = 1 # default number of max simultaneous contracts of the type
    approx_launch_cost = 0 # default approximate cost of launch to calculate launch-recover refund
    flight_level = 10000 # default altitude of the flight for Kramax AutoPilot flight plan

    @classmethod
    def get_flight_type(cls):
        contract_type = re.match(r'(.*)FlightContract', cls.__name__).group(1)
        return re.sub(r'([A-Z])', r' \1', contract_type).strip().lower()

    def __init__(self, objective=None, special_notes=None, beacons=None):
        """
        @param objective Objective of the flight (displaying in description).
        @param special_notes Special notes about the flight (displaying under
                             objective as a separate paragraph).
        @param beacons Beacons to visit when building flight plan.
        """
        self.objective = objective
        self.special_notes = special_notes
        self.beacons = [(name, BEACONS[name]) for name in beacons] if beacons else []
        self.waypoints = []
        self.from_loc = None
        self.to_loc = None

    @property
    def refund_amount(self):
        """
        Calculates amount of funds we must return to player
        to compensate launch-recover difference.
        """
        overall_percent = 100 - self.from_loc.launch_refund - self.to_loc.recovery_factor
        return max(0, self.approx_launch_cost * overall_percent / 100.0)

    def __str__(self):
        return '<{} from "{}" to "{}">'.format(self.__class__.__name__, self.from_loc, self.to_loc)

    def set_locations(self, from_loc, to_loc):
        """
        Sets departure and destination of flight and some internal flags.
        @param from_loc Start location of the flight.
        @param to_loc Destionation of the flight.
        """
        self.from_loc = from_loc
        self.to_loc = to_loc
        self.plane_allowed = (
            self.from_loc.aircraft_launch is not None and
            self.to_loc.aircraft_parking is not None
        )

    def get_description(self):
        """Returns contract description."""
        paragraphs = []
        if self.objective is not None:
            paragraphs.append('Objective: ' + self.objective)
        paragraphs.extend([
            'Departure: ' + self.from_loc.description,
            'Destination: ' + self.to_loc.description,
        ])
        if self.special_notes is not None:
            paragraphs.append('Special notes: ' + self.special_notes)
        return '\\n\\n'.join(paragraphs)

    def get_synopsis_notes(self):
        """Returns the list of the additional notes for contract synopsis."""
        dist = utils.loc_distance(self.from_loc, self.to_loc)
        notes = [
            'Distance is {} km.'.format(round(dist, 2)),
        ]
        if not self.plane_allowed:
            notes.append('You have to use helicopter or VTOL to complete this contract.')
        return notes

    def get_rewards(self):
        """
        Must be redefined to return the rewards of contract in tuple: (
            <advance funds>, <reward funds>,
            <reward reputation>, <failure reputation>,
        ).
        """
        raise NotImplementedError

    def get_data(self):
        """
        Returns data values for the storage: (<type>, <name>, <definition>).
        Empty by default, placeholder to redefine in subtypes.
        """
        return []

    def get_requirements(self):
        """
        Returns the list of contract requirements. By default requires both
        departure and destination bases exists.
        """
        requirements = []
        if self.from_loc.kk_base_name:
            requirements.append(make_base_requirement(
                'Departure', 'BaseExists',
                self.from_loc.kk_base_name,
            ))
        if self.to_loc.kk_base_name:
            requirements.append(make_base_requirement(
                'Destination', 'BaseExists',
                self.to_loc.kk_base_name,
            ))
        return requirements

    def get_waypoints(self):
        """
        Returns the list of points for waypoint generator behavior. By default
        gives parking points of destination location.
        """
        waypoints = []
        if self.to_loc.aircraft_parking:
            self.waypoints.append(self.to_loc.aircraft_parking)
            waypoints.extend([[
                    ('name', self.to_loc.name + ' aircraft parking'),
                    ('icon', ICONS_PATH + 'Parking'),
                ] + utils.point_to_params(self.to_loc.aircraft_parking)
            ])
        if self.to_loc.helipad:
            self.waypoints.append(self.to_loc.helipad)
            waypoints.extend([[
                    ('name', self.to_loc.name + ' helipad'),
                    ('icon', ICONS_PATH + 'Helipad'),
                ] + utils.point_to_params(self.to_loc.helipad)
            ])
        return waypoints

    def get_additional_behaviours(self):
        """
        Returns additional behaviours. Empty by default, placeholder to
        redefine in subtypes.
        """
        return []

    def get_parameters(self):
        """Must be redefined to return completion parameters."""
        raise NotImplementedError

    def make_takeoff_parameter(self):
        """Makes parameter that requires takeoff from the departure airport."""
        options = []
        if self.from_loc.aircraft_launch:
            options.append(make_visit_waypoint(
                self.waypoints.index(self.from_loc.aircraft_launch),
                self.from_loc.aircraft_launch_allowed_distance,
                'Start the takeoff of your plane at the beginning of the runway of the {}'.format(self.from_loc.name),
                once=True,
            ))
        if self.from_loc.helipad:
            options.append(make_visit_waypoint(
                self.waypoints.index(self.from_loc.helipad), 20,
                'Takeoff your VTOL vessel from the helipad of the {}'.format(self.from_loc.name),
                once=True,
            ))

        if len(options) < 2:
            options[0][1].append(('completeInSequence', 'true'))
            return options[0]

        options.insert(0, ('completeInSequence', 'true'))
        return make_options_group('Takeoff your vessel at the starting point. You have options', options)

    def make_land_parameter(self):
        """Makes parameter that requires landing at the destination airport."""
        options = []
        if self.to_loc.aircraft_parking:
            options.append(make_visit_waypoint(
                self.waypoints.index(self.to_loc.aircraft_parking), 35,
                'Land your plane to the runway of the {} and drive it to the parking'.format(self.to_loc.name),
            ))
        if self.to_loc.helipad:
            options.append(make_visit_waypoint(
                self.waypoints.index(self.to_loc.helipad), 20,
                'Land your VTOL vessel to the helipad of the {}'.format(self.to_loc.name),
            ))

        if len(options) < 2:
            options[0][1].append(('completeInSequence', 'true'))
            return options[0]

        options.insert(0, ('completeInSequence', 'true'))
        return make_options_group('Reach the destination. You have options', options)


class PassengersContract(Contract):
    """
    Base class for contract types in which player must transport passengers.
    Adds spawning of passengers and requires visiting start location.
    """
    passengers_number = (0, 0) # stupid default interval (subclasses must set normal one)

    def get_synopsis_notes(self):
        """Adds info about passengers count."""
        notes = [
            'You will have @/passengersNum passengers.'
        ]
        return notes + super(PassengersContract, self).get_synopsis_notes()

    def get_data(self):
        """Adds variable with passengers selection."""
        data = super(PassengersContract, self).get_data()
        data.append(('int', 'passengersNum', 'Random({}, {})'.format(*self.passengers_number)))
        data.append(('List<Kerbal>', 'passengers', 'NewKerbals(@/passengersNum)'))
        return data

    def get_requirements(self):
        """Adds requirement for departure base to be opened."""
        requirements = super(PassengersContract, self).get_requirements()
        if self.from_loc.kk_base_name:
            requirements.append(make_base_requirement(
                'Departure', 'BaseOpen',
                self.from_loc.kk_base_name,
            ))
        return requirements

    def get_waypoints(self):
        """Adds possible starting points to the list."""
        waypoints = super(PassengersContract, self).get_waypoints()
        if self.from_loc.aircraft_launch:
            self.waypoints.append(self.from_loc.aircraft_launch)
            waypoints.extend([[
                    ('name', self.from_loc.name + ' runway'),
                    ('icon', ICONS_PATH + 'Runway'),
                ] + utils.point_to_params(self.from_loc.aircraft_launch)
            ])
        if self.from_loc.helipad:
            self.waypoints.append(self.from_loc.helipad)
            waypoints.extend([[
                    ('name', self.from_loc.name + ' helipad'),
                    ('icon', ICONS_PATH + 'Helipad'),
                ] + utils.point_to_params(self.from_loc.helipad)
            ])
        return waypoints

    def get_additional_behaviours(self):
        """Adds spawn passengers behaviour."""
        behaviours = super(PassengersContract, self).get_additional_behaviours()
        behaviours.append([
            ('name', 'SpawnPassengers'),
            ('type', 'SpawnPassengers'),
            ('kerbal', '@/passengers'),
        ])
        return behaviours

    def get_parameters(self):
        params = [
            make_crew_request("Pilot", 1, "an aircraft commander"),
        ]
        additional_crew = self.make_additional_crew_parameters()
        if isinstance(additional_crew, list):
            params.extend(additional_crew)
        else:
            params.append(additional_crew)
        params.extend([
            make_passengers_request(passengers_number='@/passengersNum'),
            self.make_takeoff_parameter(),
            self.make_land_parameter(),
            make_stop_request(),
            make_waiting_request(),
        ])
        return [make_vessel_group(params), make_safety_request()]

    def make_additional_crew_parameters(self):
        """Must be redefined to return additional crew request parameters."""
        raise NotImplementedError


# ===== Mixins ===== #

class FixedRewardContract(Contract):
    """Mixin for contracts with generation-time reward."""

    def __init__(self, reward, **kwargs):
        """
        @param reward Reward funds (per contract).
        """
        super(FixedRewardContract, self).__init__(**kwargs)
        self.reward = reward


class TypedStaffContract(Contract):
    """Mixin for contracts with specified type of kerbals."""

    def __init__(self, staff_type, **kwargs):
        """
        @param staff_type Type of kerbal(s) in this contract (Pilot, Engineer
                          or Scientist).
        """
        super(TypedStaffContract, self).__init__(**kwargs)
        self.staff_type = staff_type


# ===== Contract classes ===== #

class ServiceFlightContract(TypedStaffContract):
    """Describes a service flight."""
    route_color = 'gold'
    max_simultaneous = 4
    approx_launch_cost = 10000
    flight_level = 4000
    passengers_number = (2, 4) # for random selection (**both** included)

    def __init__(self, **kwargs):
        """
        Selects passengers number for the contract. This selection must be in
        contract script itself, but currently it is not supported. For details
        see https://github.com/jrossignol/ContractConfigurator/issues/401
        """
        super(ServiceFlightContract, self).__init__(**kwargs)
        self.passengers_number = randint(*self.passengers_number)

    def set_locations(self, from_loc, to_loc):
        """Performs additional check."""
        super(ServiceFlightContract, self).set_locations(from_loc, to_loc)
        assert self.from_loc.staff_spawn is not None, \
            '{} is incorrect: origin base does not have staff spawn point'.format(self)

    def get_synopsis_notes(self):
        """Adds info about passengers count."""
        notes = [
            'You will have {} passengers.'.format(self.passengers_number),
        ]
        return notes + super(ServiceFlightContract, self).get_synopsis_notes()

    def get_rewards(self):
        reward = 20 * utils.loc_distance(self.from_loc, self.to_loc)
        return (0.2 * reward, 0.8 * reward, 0, 2)

    def get_data(self):
        """Adds variable with all passengers."""
        data = super(ServiceFlightContract, self).get_data()
        data.append(('List<Kerbal>', 'passengers', 'NewKerbals({}, "{}")'.format(
            self.passengers_number, self.staff_type,
        )))
        return data

    def get_waypoints(self):
        """Adds random waypoints for staff."""
        waypoints = super(ServiceFlightContract, self).get_waypoints()
        self.staff_points_start_index = len(waypoints)
        waypoints.extend([
            [
                ('name', 'Staff spawn point'),
                ('hidden', 'true'),
            ] + utils.point_to_params(self.from_loc.staff_spawn, absolute_altitude=True),
            [
                ('hidden', 'true'),
                ('nearIndex', self.staff_points_start_index),
                ('altitude', self.from_loc.staff_spawn[2].absolute),
                ('count', self.passengers_number),
                ('minDistance', 1),
                ('maxDistance', 2),
            ],
        ])
        self.staff_points_start_index += 1 # skip staff spawn point itself
        return waypoints

    def get_additional_behaviours(self):
        """Adds spawn staff behavior."""
        behaviours = super(ServiceFlightContract, self).get_additional_behaviours()
        spawn_staff_behaviour = [
            ('name', 'SpawnPassengers'),
            ('type', 'SpawnKerbal'),
        ]
        for kerb_num in xrange(self.passengers_number):
            wp_link = '@/WaypointGenerator.Waypoints().ElementAt({})'.format(
                self.staff_points_start_index + kerb_num
            )
            spawn_staff_behaviour.append(('KERBAL', [
                ('kerbal', '@/passengers.ElementAt({})'.format(kerb_num)),
                ('owned', 'false'),
                ('addToRoster', 'false'),
                ('lat', '{}.Latitude()'.format(wp_link)),
                ('lon', '{}.Longitude()'.format(wp_link)),
                ('alt', '{}.Altitude()'.format(wp_link)),
            ]))
        behaviours.append(spawn_staff_behaviour)
        return behaviours

    def get_parameters(self):
        params = [
            make_crew_request("Pilot", 1, "an aircraft commander"),
            make_passengers_request(),
            self.make_land_parameter(),
            make_stop_request(),
            make_waiting_request(),
        ]
        return [make_vessel_group(params), make_safety_request()]


class BusinessFlightContract(FixedRewardContract, TypedStaffContract):
    """Describes a business flight."""
    route_color = 'tomato'
    max_simultaneous = 2
    flight_level = 4000
    approx_launch_cost = 10000
    agent = 'Kerbal Aircraft Rent'

    def set_locations(self, from_loc, to_loc):
        """Performs additional check."""
        super(BusinessFlightContract, self).set_locations(from_loc, to_loc)
        assert self.from_loc.vip_spawn is not None, \
            '{} is incorrect: origin base does not have VIP spawn point'.format(self)

    def get_rewards(self):
        return (0, self.reward, 1, 3)

    def get_data(self):
        """Adds variable with passengers number selection."""
        data = super(BusinessFlightContract, self).get_data()
        data.append(('Kerbal', 'VIK', 'NewKerbalWithTrait("{}")'.format(self.staff_type)))
        data.append(('string', 'VIKwho', '@/VIK.Gender() == "Male" ? "he" : "she"'))
        data.append(('string', 'VIKwhom', '@/VIK.Gender() == "Male" ? "him" : "her"'))
        data.append(('List<Kerbal>', 'passengers', '[ @/VIK ]'))
        return data

    def get_additional_behaviours(self):
        """Adds spawn VIK behavior."""
        behaviours = super(BusinessFlightContract, self).get_additional_behaviours()
        behaviours.append([
            ('name', 'SpawnPassengers'),
            ('type', 'SpawnKerbal'),
            ('KERBAL', [
                ('kerbal', '@/VIK'),
                ('owned', 'false'),
                ('addToRoster', 'false'),
                ('lat', '{}'.format(self.from_loc.vip_spawn[0])),
                ('lon', '{}'.format(self.from_loc.vip_spawn[1])),
                ('alt', '{}'.format(self.from_loc.vip_spawn[2].absolute)),
            ]),
        ])
        return behaviours

    def get_parameters(self):
        params = [
            make_crew_request("Pilot", 1, "an aircraft commander"),
            make_crew_request("Engineer", 1, "a flight engineer"),
            make_passengers_request(),
            self.make_land_parameter(),
            make_stop_request(),
            make_waiting_request(),
        ]
        return [make_vessel_group(params), make_safety_request()]


class TouristGroupFlightContract(FixedRewardContract, PassengersContract):
    """Describes a tourists charter flight."""
    route_color = 'limegreen'
    approx_launch_cost = 15000
    flight_level = 3000
    agent = 'Kerbal Aircraft Rent'
    passengers_number = (3, 6) # for random selection (min included, max excluded)

    def get_rewards(self):
        second_crew_member_multiplier = '{} * (1.0 + 0.15 * @/needSecondCrewMember)'
        return (
            second_crew_member_multiplier.format(0.75 * self.reward),
            second_crew_member_multiplier.format(0.25 * self.reward),
            1, 3,
        )

    def get_data(self):
        """Adds variable with random second crew member flag."""
        data = super(TouristGroupFlightContract, self).get_data()
        data.append(('int', 'needSecondCrewMember', 'Random(0, 1)'))
        return data

    def make_additional_crew_parameters(self):
        return make_options_group(
            'Has at least one of these crew members', [
                ('count', '@/needSecondCrewMember'),
                ('hidden', '(@/needSecondCrewMember == 0)'),
                ('hideChildren', '(@/needSecondCrewMember == 0)'),
                make_crew_request("Pilot", 2, "a second pilot"),
                make_crew_request("Engineer", 1, "a flight engineer"),
            ],
            type='AtLeast',
        )


class CharterFlightContract(PassengersContract):
    """Describes a charter flight."""
    route_color = 'blue'
    max_simultaneous = 3
    approx_launch_cost = 30000
    flight_level = 6000
    agent = 'Kerbin Charter Jet'
    passengers_number = (8, 17) # for random selection (min included, max excluded)

    def get_rewards(self):
        dist = utils.loc_distance(self.from_loc, self.to_loc)
        return ('{} * @/passengersNum'.format(1.5 * dist), 0, 2, 4)

    def make_additional_crew_parameters(self):
        return make_options_group('Has at least one of these crew members', [
            make_crew_request("Pilot", 2, "a second pilot"),
            make_crew_request("Engineer", 1, "a flight engineer"),
        ])


class CommercialFlightContract(PassengersContract):
    """Describes a commercial flight."""
    route_color = 'skyblue'
    max_simultaneous = 4
    approx_launch_cost = 90000
    flight_level = 8000
    agent = 'BlueSky Airways'
    passengers_number = (24, 65) # for random selection (min included, max excluded)

    def get_rewards(self):
        dist = utils.loc_distance(self.from_loc, self.to_loc)
        half_reward = '{} * @/passengersNum'.format(0.6 * dist)
        return (half_reward, half_reward, 3, 5)

    def make_additional_crew_parameters(self):
        return [
            make_crew_request("Pilot", 2, "a second pilot"),
            make_crew_request("Engineer", 1, "a flight engineer"),
        ]


# ===== Parameters helpers ===== #

def make_base_requirement(target, type, base):
    return ('REQUIREMENT', [
        ('name', target + type),
        ('type', type),
        ('basename', base),
    ])

def make_options_group(description, inner, type='Any'):
    return ('PARAMETER', [
        ('name', type),
        ('type', type),
        ('title', description),
        ('disableOnStateChange', 'false'),
    ] + inner)

def make_vessel_group(inner):
    return ('PARAMETER', [
        ('name', 'VesselParameterGroup'),
        ('type', 'VesselParameterGroup'),
        ('title', 'Perform a flight'),
    ] + inner)

def make_crew_request(trait, count, whois):
    return ('PARAMETER', [
        ('name', 'HasCrew'),
        ('type', 'HasCrew'),
        ('trait', trait),
        ('minCrew', count),
        ('excludeKerbal', '@/passengers'),
        ('title', 'Has {} aboard'.format(whois)),
        ('disableOnStateChange', 'false'),
        ('hideChildren', 'true'),
    ])

def make_passengers_request(passengers_number=None):
    title = 'Has all {} passengers aboard'.format(
        passengers_number if passengers_number is not None else ''
    )
    param = ('PARAMETER', [
        ('name', 'HasPassengers'),
        ('type', 'HasCrew'),
        ('title', title.replace('  ', ' ')),
        ('disableOnStateChange', 'false'),
        ('kerbal', '@/passengers'),
    ])
    if passengers_number is not None:
        param[1].append(('hideChildren', 'true'))
    return param

def make_visit_waypoint(index, distance, reason, once=False):
    return ('PARAMETER', [
        ('name', 'VisitWaypoint'),
        ('type', 'VisitWaypoint'),
        ('index', index),
        ('distance', distance),
        ('title', reason),
        ('disableOnStateChange', str(once).lower()),
    ])

def make_stop_request():
    return ('PARAMETER', [
        ('name', 'ReachState'),
        ('type', 'ReachState'),
        ('maxSpeed', '0.0'),
        ('situation', 'LANDED'),
        ('title', 'Stop your vessel completely'),
        ('disableOnStateChange', 'false'),
        ('completeInSequence', 'true'),
        ('hideChildren', 'true'),
    ])

def make_waiting_request():
    return ('PARAMETER', [
        ('name', 'Duration'),
        ('type', 'Duration'),
        ('duration', '30s'),
        ('preWaitText', 'Wait for the passengers to exit'),
        ('waitingText', 'Waiting for the passengers to exit'),
        ('completionText', 'The passengers left the board'),
        ('disableOnStateChange', 'false'),
        ('completeInSequence', 'true'),
    ])

def make_safety_request():
    return ('PARAMETER', [
        ('name', 'KerbalDeaths'),
        ('type', 'KerbalDeaths'),
        ('title', 'Flight must be safe (avoid killing passengers)'),
        ('hideChildren', 'true'),
        ('kerbal', '@/passengers'),
    ])
