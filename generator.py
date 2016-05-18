#!/usr/bin/env python
"""Generates contract files based on locations and routes."""

import os
import re
import argparse

try:
    import svgwrite
except ImportError:
    svgwrite = None

import utils
from locations import LOCATIONS
from routes import ROUTES

RECOVER_REFUND_COEF = 0.2 # Coefficient to refund the player his loss of money via launch-recover

CFG_FILE_HEADER = """\
// This file was automatically generated via Kerbin Side GAP contracts generator.
// Do not edit it manually, all changes will be lost. Edit generator instead and rerun it to get the new file.
"""


def make_distance_table(options):
    """Makes CVS table with distances between all locations."""
    print 'Location distances table is generating'
    rows = [['Distances']]
    for loc1 in LOCATIONS:
        row = [loc1.name]
        rows[0].append(loc1.name)
        for loc2 in LOCATIONS:
            d = utils.distance(loc1, loc2)
            row.append(str(round(d, 2)))
        rows.append(row)
    if options.verbose > 1:
        print 'Writing file Distances.csv'
    with open('Distances.csv', 'w') as out:
        out.write('\n'.join([','.join(row) for row in rows]) + '\n')


def make_reward_table(options):
    """Makes CVS table with rewards for all contracts."""
    print 'Reward table is generating'
    locations_info = {
        loc.name: loc
        for loc in LOCATIONS
    }
    rows = [['Class', 'Departure', 'Destination', 'Distance', 'Min reward', 'Max reward']]
    for route, contract in ROUTES.iteritems():
        contract.set_locations(locations_info[route[0]], locations_info[route[1]])
        advance_funds, reward_funds, _, _ = contract.get_rewards()

        if options.verbose > 0:
            print 'Calculating reward for {}'.format(contract)
        reward_str = '{} + ({} + {}) * Random(1.0, 1.15)'.format(
            advance_funds, reward_funds,
            RECOVER_REFUND_COEF * contract.approx_launch_cost,
        )
        min_reward = utils.calculate_reward(contract, reward_str, calc_min=True)
        max_reward = utils.calculate_reward(contract, reward_str, calc_min=False)

        rows.append([
            contract.__class__.__name__,
            contract.from_loc.name,
            contract.to_loc.name,
            str(round(utils.distance(contract.from_loc, contract.to_loc), 2)),
            str(min_reward),
            str(max_reward),
        ])
    if options.verbose > 1:
        print 'Writing file Rewards.csv'
    with open('Rewards.csv', 'w') as out:
        out.write('\n'.join([','.join(row) for row in rows]) + '\n')


def make_route_map(options):
    """Makes SVG map with all locations and routes."""
    if svgwrite is None:
        print 'Package "svgwrite" is required to generate a map!'
        return

    print 'Routes map is generating'
    locations_on_map = {
        loc.name: utils.point_on_map(loc.position)
        for loc in LOCATIONS
    }
    route_map = svgwrite.Drawing('Routes.svg', size=(utils.MAP_WIDTH, utils.MAP_HEIGHT))
    for route, contract in ROUTES.iteritems():
        utils.add_arrow(
            route_map,
            locations_on_map[route[0]], locations_on_map[route[1]],
            stroke=contract.route_color, stroke_width=(str(utils.MAP_LINE_WIDTH) + 'px'),
        )
    for loc in LOCATIONS:
        pt = locations_on_map[loc.name]
        right_text = (pt[0] < 0.9 * utils.MAP_WIDTH)
        text_y_offset = 2.25
        if loc.name == 'Ben Bay':
            # I don't know how to fix overlapping of Kerman Lake better.
            text_y_offset = -1.25
        route_map.add(route_map.circle(center=pt, r=utils.MAP_POINT_RADIUS))
        route_map.add(route_map.text(
            loc.name,
            insert=(
                pt[0] + (4 if right_text else -4) * utils.MAP_POINT_RADIUS,
                pt[1] + text_y_offset * utils.MAP_POINT_RADIUS,
            ),
            text_anchor=('start' if right_text else 'end'),
            font_size='2em',
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
        if hasattr(contract, 'weight'):
            contract_config.append(('weight', contract.weight))

        # Add contract texts.
        contract_type = re.match(r'(.*)FlightContract', contract.__class__.__name__).group(1)
        flight_type = re.sub(r'([A-Z])', r' \1', contract_type).strip().lower()
        flight_synopsis = 'Perform {} flight from the {} to the {}.'.format(
            flight_type, contract.from_loc.name, contract.to_loc.name
        )
        contract_config.extend([
            ('title', 'Perform {} flight'.format(flight_type)),
            ('description', contract.get_description()),
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
                RECOVER_REFUND_COEF * contract.approx_launch_cost,
                reward_funds
            )),
            ('rewardScience', 0),
        ])

        # Add data nodes.
        contract_config.extend(
            ('DATA', [('type', type), (name, definition)])
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
            out.write('\n')

    groups_config = [
        ('name', 'KerbinSideGapContract'),
        ('minVersion', '1.9.6'),
        ('maxSimultaneous', 5),
    ]
    for contract_class in classes_set:
        groups_config.append(('CONTRACT_GROUP', [
            ('name', 'KerbinSideGap' + contract_class.__name__),
            ('maxSimultaneous', contract_class.max_simultaneous),
        ]))
    if options.verbose > 1:
        print 'Writing file Groups.cfg'
    with open('Groups.cfg', 'w') as out:
        out.write(CFG_FILE_HEADER)
        utils.write_config(out, [('CONTRACT_GROUP', groups_config)])
        out.write('\n')

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
        help='Make only distances table for locations.')
    parser.add_argument('--reward', action='store_true',
        help='Make only reward table for contracts.')
    parser.add_argument('--map', action='store_true',
        help='Make only routes map.')
    options = parser.parse_args()

    if options.dir is not None:
        os.chdir(options.dir)

    print 'Found {} locations, {} routes'.format(len(LOCATIONS), len(ROUTES))
    if options.dist:
        make_distance_table(options)
    elif options.reward:
        make_reward_table(options)
    elif options.map:
        make_route_map(options)
    else:
        make_routes(options)

if __name__ == '__main__':
    main()
