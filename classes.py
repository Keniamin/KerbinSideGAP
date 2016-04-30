import re
from random import randint

import utils

ICONS_PATH = 'ContractPacks/KerbinSideGAP/Icons/'


# ===== Basic classes ===== #

class Location(object):
    """Totally describes separate location at Kerbin."""

    def __init__(
        self, name, description,
        runway=None, helipad=None, aircraft_parking=None,
        staff_spawn=None, vip_spawn=None,
    ):
        """
        @param name Short name of the location.
        @param description Full description of the location.
        @param runway Runway waypoint (point where craft spawns when the player
                      selects location's runway as a launch site).
        @param helipad Helipad waypoint (point where craft spawns when the
                       player selects location's helipad as a launch site).
        @param aircraft_parking Point at which aircraft must be parked to
                                complete the contract (helipad would be another
                                one, if available). By default equals to the
                                runway. Useful if you want to move marker to
                                the part of the base which looks like a better
                                place for parking (for example, at the KSC it
                                may be a concrete pad between the runway and
                                the Space Plane Hangar).
        @param staff_spawn Point around which staff Kerbals would appear for
                           the service contracts from this location (if any).
        @param vip_spawn Point at which VIP Kerbal would appear for the
                         business flight contracts from this location (if any).
        """
        self.name = name
        self.description = description
        self.runway = runway
        self.helipad = helipad
        self.aircraft_parking = aircraft_parking
        self.staff_spawn = staff_spawn
        self.vip_spawn = vip_spawn
        if aircraft_parking is None:
            self.aircraft_parking = self.runway

    @property
    def position(self):
        return self.helipad or self.runway

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

    def __init__(self, objective=None, special_notes=None):
        """
        @param objective Objective of the flight (displaying in description).
        @param special_notes Special notes about the flight (displaying under
                             objective as a separate paragraph).
        @param additional_reward Additional reward funds (per contract).
        """
        self.objective = objective
        self.special_notes = special_notes
        self.waypoints = []
        self.from_loc = None
        self.to_loc = None

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
            self.from_loc.runway is not None and
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
        dist = utils.distance(self.from_loc, self.to_loc)
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

    def get_waypoints(self):
        """
        Returns the list of points for waypoint generator behavior. By default
        gives parking points of destination location.
        """
        waypoints = []
        if self.to_loc.aircraft_parking:
            self.waypoints.append(self.to_loc.aircraft_parking)
            waypoints += [[
                    ('name', self.to_loc.name + ' aircraft parking'),
                    ('icon', ICONS_PATH + 'Parking'),
                ] + utils.point_to_params(self.to_loc.aircraft_parking)
            ]
        if self.to_loc.helipad:
            self.waypoints.append(self.to_loc.helipad)
            waypoints += [[
                    ('name', self.to_loc.name + ' helipad'),
                    ('icon', ICONS_PATH + 'Helipad'),
                ] + utils.point_to_params(self.to_loc.helipad)
            ]
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
        if self.from_loc.runway:
            options.append(make_visit_waypoint(
                self.waypoints.index(self.from_loc.runway), 20,
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
    weight = 0.85
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

    def get_waypoints(self):
        """Adds possible starting points to the list."""
        waypoints = super(PassengersContract, self).get_waypoints()
        if self.from_loc.runway:
            self.waypoints.append(self.from_loc.runway)
            waypoints += [[
                    ('name', self.from_loc.name + ' runway'),
                    ('icon', ICONS_PATH + 'Runway'),
                ] + utils.point_to_params(self.from_loc.runway)
            ]
        if self.from_loc.helipad:
            self.waypoints.append(self.from_loc.helipad)
            waypoints += [[
                    ('name', self.from_loc.name + ' helipad'),
                    ('icon', ICONS_PATH + 'Helipad'),
                ] + utils.point_to_params(self.from_loc.helipad)
            ]
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
        self.passenger_engineers = (1 if staff_type == 'Engineer' else 0)
        self.passenger_pilots = (1 if staff_type == 'Pilot' else 0)
        self.staff_type = staff_type


# ===== Contract classes ===== #

class ServiceFlightContract(TypedStaffContract):
    """Describes a service flight."""
    route_color = 'gold'
    max_simultaneous = 2
    approx_launch_cost = 10000
    passengers_number = (2, 4) # for random selection (**both** included)

    def __init__(self, **kwargs):
        """
        Selects passengers number for the contract. This selection must be in
        contract script itself, but currently it is not supported. For details
        see https://github.com/jrossignol/ContractConfigurator/issues/401
        """
        super(ServiceFlightContract, self).__init__(**kwargs)
        self.passengers_number = randint(*self.passengers_number)
        self.passenger_engineers *= self.passengers_number
        self.passenger_pilots *= self.passengers_number

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
        reward = 20 * utils.distance(self.from_loc, self.to_loc)
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
        waypoints += [
            [
                ('name', 'Staff spawn point'),
                ('hidden', 'true'),
            ] + utils.point_to_params(self.from_loc.staff_spawn),
            [
                ('hidden', 'true'),
                ('nearIndex', self.staff_points_start_index),
                ('altitude', self.from_loc.staff_spawn[2]),
                ('count', self.passengers_number),
                ('minDistance', 1),
                ('maxDistance', 2),
            ],
        ]
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
            make_crew_request("Pilot", 1 + self.passenger_pilots, "an aircraft commander"),
            make_passengers_request(),
            self.make_land_parameter(),
            make_stop_request(),
            make_waiting_request(),
        ]
        return [make_vessel_group(params), make_safety_request()]


class BusinessFlightContract(FixedRewardContract, TypedStaffContract):
    """Describes a business flight."""
    route_color = 'tomato'
    weight = 0.6
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
                ('alt', '{}'.format(self.from_loc.vip_spawn[2])),
            ]),
        ])
        return behaviours

    def get_parameters(self):
        params = [
            make_crew_request("Pilot", 1 + self.passenger_pilots, "an aircraft commander"),
            make_crew_request("Engineer", 1 + self.passenger_engineers, "a flight engineer"),
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
    max_simultaneous = 2
    approx_launch_cost = 30000
    agent = 'Kerbin Charter Jets'
    passengers_number = (8, 17) # for random selection (min included, max excluded)

    def get_rewards(self):
        dist = utils.distance(self.from_loc, self.to_loc)
        return ('{} * @/passengersNum'.format(1.5 * dist), 0, 2, 4)

    def make_additional_crew_parameters(self):
        return make_options_group('Has at least one of these crew members', [
            make_crew_request("Pilot", 2, "a second pilot"),
            make_crew_request("Engineer", 1, "a flight engineer"),
        ])


class CommercialFlightContract(PassengersContract):
    """Describes a commercial flight."""
    route_color = 'skyblue'
    max_simultaneous = 2
    approx_launch_cost = 90000
    agent = 'Kerbin BlueSky Airlines'
    passengers_number = (24, 65) # for random selection (min included, max excluded)

    def get_rewards(self):
        dist = utils.distance(self.from_loc, self.to_loc)
        half_reward = '{} * @/passengersNum'.format(0.6 * dist)
        return (half_reward, half_reward, 3, 5)

    def make_additional_crew_parameters(self):
        return [
            make_crew_request("Pilot", 2, "a second pilot"),
            make_crew_request("Engineer", 1, "a flight engineer"),
        ]


# ===== Parameters helpers ===== #

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
