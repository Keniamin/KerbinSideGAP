#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generates contract files based on locations and routes."""

import os
import re
import argparse

try:
    import svgwrite
except ImportError:
    svgwrite = None

import utils
import geometry
import flightplan
from classes import DEFAULT_AGENT
from locations import LOCATIONS
from beacons import BEACONS
from routes import ROUTES

CFG_FILE_HEADER = """\
// This file was automatically generated via Kerbin Side GAP contracts generator.
// Do not edit it manually, all changes will be lost. Edit generator instead and rerun it to get the new file.
"""


def _for_all_runways(callback):
    """Applies a callback to all allowed runways of all locations."""
    for loc in LOCATIONS:
        if not loc.runways or loc.name == "Kerbal Space Centre":
            continue
        for runway_num, (ep1, ep2) in enumerate(loc.runways):
            for gs_pt, loc_pt in [(ep1, ep2), (ep2, ep1)]:
                if gs_pt[3] is None:
                    continue
                callback(loc, runway_num, gs_pt, loc_pt)
    return None


def _make_kramax_patch(plans_list):
    """Formats Kramax Autopilot plans in a proper patch."""
    return [(
        '@KramaxAutoPilotPlansDefault:NEEDS[KramaxAutoPilot]', [(
            '@Kerbin', plans_list
        )],
    )]


def make_distance_table(options):
    """Makes .csv table with distances between all locations."""
    print 'Location distances table is generating'
    rows = [['Distances']]
    for loc1 in LOCATIONS:
        row = [loc1.name]
        rows[0].append(loc1.name)
        for loc2 in LOCATIONS:
            dist = utils.loc_distance(loc1, loc2)
            row.append(str(round(dist, 2)))
        rows.append(row)
    if options.verbose > 1:
        print 'Writing file Distances.csv'
    with open('Distances.csv', 'w') as out:
        out.write('\n'.join([','.join(row) for row in rows]) + '\n')


def make_locations_waypoints(options):
    """Makes .cfg file with all waypoints in WaypointManager format."""
    print 'Waypoints for locations are generating'
    waypoints = []
    index = 0
    for loc in LOCATIONS:
        for point_type in ('helipad', 'aircraft_launch', 'aircraft_parking', 'staff_spawn', 'vip_spawn'):
            point = getattr(loc, point_type)
            if point is None or (point_type == 'aircraft_parking' and point == loc.aircraft_launch):
                continue
            index += 1
            waypoints.append(('WAYPOINT', [
                    ('name', '{} > {}'.format(loc.name, point_type)),
                    ('celestialName', 'Kerbin'),
                    ('icon', 'report'),
                    ('index', index),
                ] + utils.point_to_params(point)
            ))
    if options.verbose > 1:
        print 'Writing file CustomWaypoints.cfg'
    with open('CustomWaypoints.cfg', 'w') as out:
        utils.write_config(out, waypoints)


def make_locations_runways(options):
    """Makes .rwy file with all runways in NavUtilities format."""
    print 'Runways for locations are generating'
    runways = {}

    @_for_all_runways
    def _(loc, runway_num, gs_pt, loc_pt):
        hdg = geometry.heading(gs_pt, loc_pt)
        hdg_str = '{:02}'.format(int(round(hdg / 10)))
        name = '{} {}'.format(re.sub(r'[^a-zA-Z0-9 ]', '°', loc.name), hdg_str)
        if gs_pt[3] > 0:
            name = '{} gs {}'.format(name, gs_pt[3])
        short_name = '{}{}'.format(
            ''.join(word[0] for word in re.sub(r'([A-Z])', r' \1', loc.name).split()),
            hdg_str,
        )
        runway_key = (loc.name, runway_num)
        runways.setdefault(runway_key, {})[name] = [
            ('body', 'Kerbin'),
            ('ident', name),
            ('shortID', short_name),
            ('hdg', round(hdg, 2)),
            ('altMSL', gs_pt[2]),
            ('gsLatitude', gs_pt[0]),
            ('gsLongitude', gs_pt[1]),
            ('locLatitude', loc_pt[0]),
            ('locLongitude', loc_pt[1]),
            ('outerMarkerDist', 10000),
            ('middleMarkerDist', 2200),
            ('innerMarkerDist', 200),
        ]

    config = []
    for runway_key in sorted(runways):
        loc_runways = runways[runway_key]
        if len(loc_runways) == 2:
            names = loc_runways.keys()
            loc_runways[names[0]].append(('identOfOpposite', names[1]))
            loc_runways[names[1]].append(('identOfOpposite', names[0]))
        config.extend(('Runway', loc_runways[name]) for name in sorted(loc_runways))
    if options.verbose > 1:
        print 'Writing file KerbinSideRunways.rwy'
    with open('KerbinSideRunways.rwy', 'w') as out:
        out.write(CFG_FILE_HEADER)
        utils.write_config(out, config)


def make_landing_patterns(options):
    """Makes .cfg file with all landing patterns for Kramax AutoPilot."""
    print 'Landing patterns are generating'
    landing_patterns = {}

    @_for_all_runways
    def _(loc, runway_num, gs_pt, loc_pt):
        hdg = geometry.heading(gs_pt, loc_pt)
        name = 'Landing {} {:02}'.format(loc.name, int(round(hdg / 10)))
        description = 'Plan for landing to the {} with heading {}°'.format(
            loc.name, int(round(hdg)),
        )
        waypoints = flightplan.make_landing_pattern(gs_pt, loc_pt)
        landing_patterns[name] = [
            ('name', name),
            ('description', description),
            ('planet', 'Kerbin'),
            ('WayPoints', [('WayPoint', waypoint) for waypoint in waypoints]),
        ]

    plans_list = [('FlightPlan', landing_patterns[name]) for name in sorted(landing_patterns)]
    if options.verbose > 1:
        print 'Writing file KerbinSideRunwaysLandingPatterns.cfg'
    with open('KerbinSideRunwaysLandingPatterns.cfg', 'w') as out:
        out.write(CFG_FILE_HEADER)
        utils.write_config(out, _make_kramax_patch(plans_list))


def make_reward_table(options):
    """Makes .csv table with rewards for all contracts."""
    print 'Reward table is generating'
    locations_dict = {loc.name: loc for loc in LOCATIONS}
    rows = [['Class', 'Departure', 'Destination', 'Distance', 'Min reward', 'Max reward']]
    for route, contract in ROUTES.iteritems():
        contract.set_locations(locations_dict[route[0]], locations_dict[route[1]])
        advance_funds, reward_funds, _, _ = contract.get_rewards()

        if options.verbose > 0:
            print 'Calculating reward for {}'.format(contract)
        reward_str = '{} + ({} + {}) * Random(1.0, 1.15)'.format(
            advance_funds, reward_funds, contract.refund_amount,
        )
        min_reward = utils.calculate_reward(contract, reward_str, calc_min=True)
        max_reward = utils.calculate_reward(contract, reward_str, calc_min=False)

        rows.append([
            contract.__class__.__name__,
            contract.from_loc.name,
            contract.to_loc.name,
            str(round(utils.loc_distance(contract.from_loc, contract.to_loc), 2)),
            str(min_reward),
            str(max_reward),
        ])
    if options.verbose > 1:
        print 'Writing file Rewards.csv'
    with open('Rewards.csv', 'w') as out:
        out.write('\n'.join([','.join(row) for row in rows]) + '\n')


def make_flight_plans(options):
    """Makes .cfg file with flight plans for Kramax AutoPilot."""
    print 'Flight plans are generating'
    locations_dict = {loc.name: loc for loc in LOCATIONS}
    flight_plans = {}
    distances = []
    for route, contract in ROUTES.iteritems():
        from_loc = locations_dict[route[0]]
        to_loc = locations_dict[route[1]]
        contract.set_locations(from_loc, to_loc)
        if not contract.plane_allowed:
            continue
        name = '{} -> {}'.format(from_loc.name, to_loc.name)
        description = 'Plan for {} flight from the {} to the {}.'.format(
            contract.get_flight_type(), from_loc.name, to_loc.name,
        )
        waypoints, beacon_distances = flightplan.make_route_waypoints(
            from_loc, to_loc, contract.flight_level, contract.beacons,
        )
        distances.append({
            'name': name,
            'type': contract.get_flight_type(),
            'straight': utils.loc_distance(from_loc, to_loc),
            'max': max(beacon_distances),
            'sum': sum(beacon_distances),
        })
        flight_plans[name] = [
            ('name', name),
            ('description', description),
            ('planet', 'Kerbin'),
            ('WayPoints', [('WayPoint', waypoint) for waypoint in waypoints]),
        ]
    plans_list = [('FlightPlan', flight_plans[name]) for name in sorted(flight_plans)]
    if options.verbose > 1:
        print 'Writing file KerbinSideGapFlightPlans.cfg'
    with open('KerbinSideGapFlightPlans.cfg', 'w') as out:
        out.write(CFG_FILE_HEADER)
        utils.write_config(out, _make_kramax_patch(plans_list))

    if options.verbose > 0:
        for info in sorted(distances, key=(lambda info: (info['type'], info['max']))):
            print 'The most distant beacons in {} km, beacons distance is {} km ({:+}% of straight) for {} flight "{}" '.format(
                round(info['max'], 1),
                round(info['sum'], 1),
                round(100 * (info['sum'] / info['straight'] - 1), 1),
                info['type'], info['name'],
            )


def make_route_map(options):
    """Makes .svg map with all locations and routes."""
    if svgwrite is None:
        print 'Package "svgwrite" is required to generate a map!'
        return

    print 'Routes map is generating'
    locations_dict = {loc.name: loc for loc in LOCATIONS}
    name = 'FlightPlans.svg' if options.beacons else 'Routes.svg'
    route_map = svgwrite.Drawing(name, size=(utils.MAP_WIDTH, utils.MAP_HEIGHT))

    for route, contract in ROUTES.iteritems():
        from_loc = locations_dict[route[0]]
        to_loc = locations_dict[route[1]]
        contract.set_locations(from_loc, to_loc)
        if options.beacons and not contract.plane_allowed:
            continue
        utils.add_route_arrow(
            route_map, from_loc, to_loc,
            beacons=(contract.beacons if options.beacons else None),
            stroke=contract.route_color,
            stroke_width='{}px'.format(utils.MAP_LINE_WIDTH),
        )
    for loc in LOCATIONS:
        pt = utils.point_on_map(loc.position)
        right_text = (pt[0] < 0.9 * utils.MAP_WIDTH)
        text_y_offset = 2.25
        if loc.name == 'Ben Bay':
            # I don't know how to fix overlapping of Kerman Lake better.
            text_y_offset = -1.25
        displace = geometry.Vector(4 if right_text else -4, text_y_offset)
        route_map.add(route_map.circle(center=pt, r=utils.MAP_POINT_RADIUS))
        route_map.add(route_map.text(
            loc.name,
            insert=(pt + displace * utils.MAP_POINT_RADIUS),
            text_anchor=('start' if right_text else 'end'),
            font_size='{}px'.format(utils.MAP_FONT_SIZE),
        ))
    if options.beacons:
        for beacon_name, beacon_pos in BEACONS.iteritems():
            pt = utils.point_on_map(beacon_pos)
            utils.add_beacon(route_map, pt)
            if any(geometry.distance(beacon_pos, loc.position) < 25 for loc in LOCATIONS):
                continue
            right_text = (pt[0] < 0.9 * utils.MAP_WIDTH)
            text_y_offset = 2.25
            if beacon_name == 'ISLAND':
                # I don't know how to fix overlapping of KSC better.
                text_y_offset = 4.25
            if beacon_name == 'SCORPION-MOUNTAINS':
                # I don't know how to fix overlapping of LONELY-MOUNTAIN better.
                right_text = False
            displace = geometry.Vector(4 if right_text else -4, text_y_offset)
            route_map.add(route_map.text(
                beacon_name,
                insert=(pt + displace * utils.MAP_POINT_RADIUS),
                text_anchor=('start' if right_text else 'end'),
                font_size='{}px'.format(0.75 * utils.MAP_FONT_SIZE),
            ))
    route_map.save()


def make_routes(options):
    """Makes contract files."""
    print 'Contract files is generating'
    locations_info = {
        loc.name: {'location': loc, 'incoming': 0, 'outgoing': 0}
        for loc in LOCATIONS
    }
    classes_set = set()
    for route, contract in ROUTES.iteritems():
        # Find and count locations.
        from_loc = locations_info[route[0]]
        to_loc = locations_info[route[1]]
        from_loc['outgoing'] += 1
        to_loc['incoming'] += 1

        # Initialize route and config.
        contract.set_locations(from_loc['location'], to_loc['location'])
        classes_set.add(contract.__class__)
        contract_config = []

        # Add common contract info.
        contract_group = 'KerbinSideGap' + contract.__class__.__name__
        contract_name = ''.join([
            contract.from_loc.alphanum_name,
            contract.to_loc.alphanum_name,
            contract.__class__.__name__,
        ])
        contract_config.extend([
            ('name', contract_name),
            ('group', contract_group),
            ('maxSimultaneous', 1),
            ('targetBody', 'Kerbin'),
            ('prestige', 'Trivial'),
            ('deadline', 3),
        ])
        if hasattr(contract, 'agent'):
            contract_config.append(('agent', contract.agent))

        # Add contract texts.
        flight_title = 'Flight: {} -> {}'.format(contract.from_loc.name, contract.to_loc.name)
        flight_description = contract.get_description()
        flight_generic_description = utils.normalize_flight_description(flight_description)
        flight_synopsis = 'Perform {} flight from the {} to the {}.'.format(
            contract.get_flight_type(), contract.from_loc.name, contract.to_loc.name,
        )
        contract_config.extend([
            ('title', flight_title),
            ('description', flight_description),
        ])
        if flight_generic_description != flight_description:
            contract_config.append(('genericDescription', flight_generic_description))
        contract_config.extend([
            ('synopsis', ' '.join([flight_synopsis] + contract.get_synopsis_notes())),
            ('completedMessage', 'Your flight successfully completed.'),
        ])

        # Add contract reward info.
        advance_funds, reward_funds, reward_reputation, failure_reputation = contract.get_rewards()
        contract_config.extend([
            ('advanceFunds', advance_funds),
            ('failureReputation', failure_reputation),
            ('failureFunds', '{} * Random(0.1, 0.25)'.format(advance_funds)),
            ('rewardReputation', reward_reputation),
            ('rewardFunds', '({} + {}) * Random(1.0, 1.15)'.format(
                reward_funds, contract.refund_amount,
            )),
            ('rewardScience', 0),
        ])

        # Add data nodes.
        contract_config.extend(
            ('DATA', [('type', type), ('hidden', 'true'), (name, definition)])
            for type, name, definition in contract.get_data()
        )

        # Add requirements.
        contract_config.extend(contract.get_requirements())

        # Add behaviours.
        waypoints_config = []
        for wp in contract.get_waypoints():
            attribute_keys = set(el[0] for el in wp)
            point_type = 'RANDOM_WAYPOINT'
            if 'nearIndex' in attribute_keys:
                point_type = 'RANDOM_WAYPOINT_NEAR'
            elif 'latitude' in attribute_keys and 'longitude' in attribute_keys:
                point_type = 'WAYPOINT'
            waypoints_config.append((point_type, wp))
        contract_config.append(('BEHAVIOUR', [
                ('name', 'WaypointGenerator'),
                ('type', 'WaypointGenerator'),
            ] + waypoints_config
        ))
        contract_config.extend(('BEHAVIOUR', beh) for beh in contract.get_additional_behaviours())

        # Add parameters.
        contract_config.extend(contract.get_parameters())

        # Write config.
        if options.verbose > 1:
            print 'Writing file {}.cfg'.format(contract_name)
        with open(contract_name + '.cfg', 'w') as out:
            out.write(CFG_FILE_HEADER)
            utils.write_config(out, [('CONTRACT_TYPE', contract_config)])

    groups_config = [
        ('minVersion', '1.21.0'),
        ('name', 'KerbinSideGapContract'),
        ('displayName', 'Kerbin Side GAP'),
        ('agent', DEFAULT_AGENT),
        ('maxSimultaneous', 8),
    ]
    for contract_class in classes_set:
        group_config = [
            ('minVersion', '1.21.0'),
            ('name', 'KerbinSideGap' + contract_class.__name__),
            ('displayName', 'Perform {} flight'.format(contract_class.get_flight_type())),
            ('agent', getattr(contract_class, 'agent', DEFAULT_AGENT)),
            ('maxSimultaneous', contract_class.max_simultaneous),
        ]
        groups_config.append(('CONTRACT_GROUP', group_config))
    if options.verbose > 1:
        print 'Writing file Groups.cfg'
    with open('Groups.cfg', 'w') as out:
        out.write(CFG_FILE_HEADER)
        utils.write_config(out, [('CONTRACT_GROUP', groups_config)])

    if options.verbose > 0:
        for loc, info in locations_info.iteritems():
            print 'Location "{}": {} incoming, {} outgoing'.format(
                loc, info['incoming'], info['outgoing']
            )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--verbose', action='count',
        help='Be more verbose. Repeate to increase.')
    parser.add_argument('-d', '--dir', type=str,
        help='Generate files in directory DIR.')
    parser.add_argument('--dist', action='store_true',
        help='Make distances table for locations.')
    parser.add_argument('--waypoints', action='store_true',
        help='Make waypoints file.')
    parser.add_argument('--runways', action='store_true',
        help='Make runways file.')
    parser.add_argument('--landing-patterns', action='store_true',
        help='Make landing patterns.')
    parser.add_argument('--rewards', action='store_true',
        help='Make rewards table for contracts.')
    parser.add_argument('--flight-plans', action='store_true',
        help='Make flight plans for contracts.')
    parser.add_argument('--map', action='store_true',
        help='Make routes map.')
    parser.add_argument('--beacons', action='store_true',
        help='Make routes map with only plane routes, considering beacons.')
    parser.add_argument('--routes', action='store_true',
        help='Make routes files themselves.')
    options = parser.parse_args()

    if options.dir is not None:
        os.chdir(options.dir)

    print 'Found {} locations, {} routes'.format(len(LOCATIONS), len(ROUTES))
    if options.dist:
        make_distance_table(options)
    if options.waypoints:
        make_locations_waypoints(options)
    if options.runways:
        make_locations_runways(options)
    if options.landing_patterns:
        make_landing_patterns(options)
    if options.rewards:
        make_reward_table(options)
    if options.flight_plans:
        make_flight_plans(options)
    if options.map or options.beacons:
        make_route_map(options)
    if options.routes:
        make_routes(options)

if __name__ == '__main__':
    main()
