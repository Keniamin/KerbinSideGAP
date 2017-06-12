#!/usr/bin/env python
"""Finds launch sites in .cfg files."""

import os
import re
import sys
import argparse

import geometry

GUARANTEED_CLEAR_ALTITUDE = 500


class LaunchSiteFinder(object):
    patterns =[
        'Group', 'Category',
        'RefLatitude', 'RefLongitude', 'RadiusOffset',
        'LaunchSiteName', 'LaunchSiteDescription',
        'LaunchRefund', 'RecoveryFactor',
    ]

    @staticmethod
    def matches(config):
        """
        Heuristic function to determine whether config defines a launch site.
        """
        return (
            'RocketPad' not in config
            and re.search(r'\sLaunchSiteName = \S', config) is not None
            and re.search(r'\sLaunchPadTransform = \S', config) is not None
        )

    @staticmethod
    def format(groups):
        """Formats info about grouped bases in the proper form (returns text)."""
        text = []
        for loc in sorted(groups):
            loc_bases = sorted(groups[loc], key=(lambda base: base['Category']), reverse=True)
            bases_types = set(base['Category'] for base in loc_bases)
            if len(bases_types) != len(loc_bases):
                print >> sys.stderr, 'WARNING: Location {} has non-unique launch site types'.format(loc)
            text.extend(['Location(', '\t"{}", "<description>",'.format(loc)])
            text.extend(
                '\t# {} "{}": {}'.format(
                    base['Category'], base['LaunchSiteName'], base['LaunchSiteDescription'],
                )
                for base in loc_bases
            )
            text.extend(
                '\t{}=({}, {}, Alt({}, None)),'.format(
                    'helipad' if base['Category'] == 'Helipad' else 'aircraft_launch',
                    base['RefLatitude'], base['RefLongitude'], base['RadiusOffset'],
                )
                for base in loc_bases
            )
            for base in loc_bases:
                if 'RecoveryFactor' not in base:
                    print >> sys.stderr, 'WARNING: Location {} has no recovery factor for {}'.format(
                        loc, 'helipad' if base['Category'] == 'Helipad' else 'aircraft_launch',
                    )
                if 'LaunchRefund' not in base:
                    print >> sys.stderr, 'WARNING: Location {} has no launch refund for {}'.format(
                        loc, 'helipad' if base['Category'] == 'Helipad' else 'aircraft_launch',
                    )
            text.extend(
                '\tlaunch_refund={},'.format(base['LaunchRefund'])
                for base in loc_bases
                if int(base.get('LaunchRefund', 0))
            )
            text.extend(
                '\trecovery_factor={},'.format(base['RecoveryFactor'])
                for base in loc_bases
                if int(base.get('RecoveryFactor', 0))
            )
            text.extend('\tkk_base_name="{}",'.format(base['LaunchSiteName']) for base in loc_bases)
            text.append('),')
        return '\n'.join(text)


class RocketPadFinder(LaunchSiteFinder):
    @staticmethod
    def matches(config):
        """
        Heuristic function to determine whether config defines a rocket pad.
        """
        return (
            'RocketPad' in config
            and re.search(r'\sLaunchSiteName = \S', config) is not None
            and re.search(r'\sLaunchPadTransform = \S', config) is not None
        )


class BeaconFinder(object):
    patterns = ['Group', 'FacilityType', 'RadialPosition', 'RadiusOffset']

    @staticmethod
    def matches(config):
        """
        Heuristic function to determine whether config defines a beacon.
        """
        return re.search(r'\sFacilityType = (Tracking|Radar)Station', config) is not None

    @staticmethod
    def format(groups):
        """Formats info about grouped bases in the proper form (returns text)."""
        text = []
        for loc in sorted(groups):
            name = re.sub(r'([^A-Z])([A-Z])', r'\1-\2', loc).upper()
            for base in groups[loc]:
                pos = map(float, base['RadialPosition'].split(','))
                coords = geometry.angles_from_sphere(
                    geometry.Vector.normalize(geometry.Vector(pos[0], pos[2], pos[1]))
                )
                alt = 100 * int((float(base['RadiusOffset']) + GUARANTEED_CLEAR_ALTITUDE) / 100)
                text.append("'{}': ({}, {}, {}),".format(name, coords[0], coords[1], alt))
        return '\n'.join(text)


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


def group_bases(all_bases):
    """Groups bases to a dictionary by 'Group' parameter."""
    groups = {}
    for base in all_bases:
        group = base['Group']
        if group in groups:
            groups[group].append(base)
        else:
            groups[group] = [base]
    return groups


def main():
    finders = {
        'launch-site': LaunchSiteFinder,
        'rocket-pad': RocketPadFinder,
        'beacon': BeaconFinder,
    }

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preformat', action='store_true',
        help='Group found objects by base and preformat as Python objects')
    parser.add_argument('--finder', type=unicode, choices=finders, default='launch-site',
        help='Algorithm of finding (i.e. what kind of bases must be found)')
    parser.add_argument('dirs', metavar='PATH', type=unicode, nargs='+',
        help='Path list to find config files')
    options = parser.parse_args()

    configs = []
    for dir in options.dirs:
        configs.extend(find_configs(dir))

    bases = []
    finder = finders[options.finder]
    for name in configs:
        with open(name) as file:
            config = file.read()
        if finder.matches(config):
            site_info = (
                line.strip() for line in config.split('\n')
                if any(pattern in line for pattern in finder.patterns)
            )
            if options.preformat:
                bases.append(dict(
                    [s.strip() for s in line.split('=')]
                    for line in site_info
                ))
            else:
                print '{}:\n\t{}\n'.format(name, '\n\t'.join(site_info))
    if options.preformat:
        print finder.format(group_bases(bases))

if __name__ == '__main__':
    main()