#!/usr/bin/env python
"""Finds runways/helipads in .cfg files."""

import os
import re
import sys
import argparse

PATTERNS = [
    'RefLatitude', 'RefLongitude', 'RadiusOffset',
    'LaunchSiteName', 'LaunchSiteDescription',
    'Group', 'Category',
]


def find_configs(dir):
    """Recursively finds .cfg files in directory."""
    configs = []
    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if os.path.isdir(path):
            configs.extend(find_configs(path))
        elif os.path.isfile(path) and name.endswith('.cfg'):
            configs.append(path)
    return configs


def is_launch_site(config):
    """
    Heuristic function to determine whether config defines a runway/helipad.
    """
    return (
        re.search(r'\sLaunchPadTransform = \S', config) is not None
        and 'LaunchSiteName' in config and not 'RocketPad' in config
    )


def print_locations(all_bases):
    """
    Groups bases by a 'Group' parameter and prints
    result using Location object style.
    """
    locations = {}
    for base in all_bases:
        group = base['Group']
        if group in locations:
            locations[group].append(base)
        else:
            locations[group] = [base]
    for loc in sorted(locations):
        loc_bases = sorted(locations[loc], key=(lambda base: base['Category']), reverse=True)
        bases_types = set(base['Category'] for base in loc_bases)
        if len(bases_types) != len(loc_bases):
            print >> sys.stderr, 'WARNING: Location {} has non-unique launch site types'.format(loc)
        text = ['Location(\n\t"{}", "<description>",'.format(loc)]
        text.extend([
            '\t# {} "{}": {}'.format(
                base['Category'], base['LaunchSiteName'], base['LaunchSiteDescription'],
            )
            for base in loc_bases
        ])
        text.extend([
            '\t{}=({}, {}, {}),'.format(
                'helipad' if base['Category'] == 'Helipad' else 'runway',
                base['RefLatitude'], base['RefLongitude'], base['RadiusOffset'],
            )
            for base in loc_bases
        ])
        text.extend([
            '\tkk_base_name="{}",'.format(base['LaunchSiteName'])
            for base in loc_bases
        ])
        text.append('),')
        print '\n'.join(text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--locations', action='store_true',
        help='Group found objects by base and preformat as Location objects')
    parser.add_argument('dirs', metavar='PATH', type=unicode, nargs='+',
        help='Path list to find config files')
    options = parser.parse_args()

    configs = []
    for dir in options.dirs:
        configs.extend(find_configs(dir))

    bases = []
    for name in configs:
        with open(name) as file:
            config = file.read()
        if is_launch_site(config):
            site_info = (
                line.strip() for line in config.split('\n')
                if any(pattern in line for pattern in PATTERNS)
            )
            if options.locations:
                bases.append(dict(
                    [s.strip() for s in line.split('=')]
                    for line in site_info
                ))
            else:
                print '{}:\n\t{}\n'.format(name, '\n\t'.join(site_info))
    if options.locations:
        print_locations(bases)


if __name__ == '__main__':
    main()