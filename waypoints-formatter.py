#!/usr/bin/env python
"""
Small utility to find waypoints in CustomWaypoints.cfg from WaypointsManager.
"""

import os
import sys

PATTERNS = [
    'name', 'latitude', 'longitude', 'altitude',
]


def main():
    waypoints = []
    with open('CustomWaypoints.cfg') as file:
        config = file.read()
    for wp_config in config.split('WAYPOINT'):
        wp_info = (
            line.strip() for line in wp_config.split('\n')
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
        if 'finish' in waypoint['name']:
            wp_type = 'aircraft_parking'
        elif 'service' in waypoint['name']:
            wp_type = 'staff_spawn'
        elif 'VIP' in waypoint['name']:
            wp_type = 'vip_spawn'
        elif 'runway' in waypoint['name']:
            wp_type = 'runway'
        elif 'helipad' in waypoint['name']:
            wp_type = 'helipad'
        waypoints_info[waypoint['name']] = '{}=({}, {}, {}), # {}'.format(
            wp_type,
            waypoint['latitude'], waypoint['longitude'],
            waypoint['altitude'] if abs(float(waypoint['altitude'])) > 1e-9 else 0,
            waypoint['name'],
        )

    for waypoint in sorted(waypoints_info):
        print waypoints_info[waypoint]

if __name__ == '__main__':
    main()
