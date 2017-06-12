#!/usr/bin/env python
"""
Small utility to find waypoints in CustomWaypoints.cfg from WaypointsManager.
"""

import os
import sys
import argparse

PATTERNS = [
    'name', 'latitude', 'longitude', 'altitude',
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', metavar='FILE', type=str, help='File to parse.')
    options = parser.parse_args()

    waypoints = []
    with open(options.file) as file:
        config = file.read()
    for wp_config in config.split('WAYPOINT'):
        wp_info = (
            line.strip()
            for line in wp_config.split('\n')
            if any(pattern in line for pattern in PATTERNS)
        )
        waypoints.append(dict(
            [s.strip() for s in line.split('=')]
            for line in wp_info
        ))

    waypoints_info = {}
    for waypoint in waypoints:
        if not 'name' in waypoint:
            continue
        wp_type = 'unknown'
        if 'helipad' in waypoint['name']:
            wp_type = 'helipad'
        elif 'launch' in waypoint['name']:
            wp_type = 'aircraft_launch'
        elif 'parking' in waypoint['name']:
            wp_type = 'aircraft_parking'
        elif (
            'service' in waypoint['name']
            or 'staff' in waypoint['name']
        ):
            wp_type = 'staff_spawn'
        elif 'vip' in waypoint['name']:
            wp_type = 'vip_spawn'
        waypoints_info[waypoint['name']] = '{}=({}, {}, Alt({}, None)), # {}'.format(
            wp_type,
            waypoint['latitude'], waypoint['longitude'],
            waypoint['altitude'] if abs(float(waypoint['altitude'])) > 1e-9 else 0,
            waypoint['name'],
        )

    for waypoint in sorted(waypoints_info):
        print waypoints_info[waypoint]

if __name__ == '__main__':
    main()
