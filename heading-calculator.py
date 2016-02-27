#!/usr/bin/env python
"""
Small utility to calculate heading of runways given by endpoints.
"""

from math import sqrt, pi, acos

import utils

RUNWAYS = {
    # '<name>': [<heading more than 180 degrees>, <ground contact point>, <opposite end point>],
    'Test 1': [False, (22.8284, 238.9345), (22.70469, 239.0598)],
    'Test 2': [True, (22.70469, 239.0598), (22.8284, 238.9345)],
}


def chord_to_tangent(pt0, pt1):
    """
    Returns the tangent vector for sphere in the direction of the given chord.
    """
    chord = tuple(pair[1]-pair[0] for pair in zip(pt0, pt1))
    coef = sum(pair[0]*pair[1] for pair in zip(pt0, chord))
    tangent = tuple(pair[1] - coef*pair[0] for pair in zip(pt0, chord))
    norm = sqrt(sum(coord ** 2 for coord in tangent))
    return tuple(coord / norm for coord in tangent)


def get_heading(more_than_straight, angles1, angles2):
    """Returns heading of the runway."""
    pt0 = utils.point_on_sphere(angles1)
    pt1 = utils.point_on_sphere(angles2)
    pt2 = utils.point_on_sphere((0.5*pi, 0))
    v1 = chord_to_tangent(pt0, pt1)
    v2 = chord_to_tangent(pt0, pt2)
    ang = 180 * acos(sum(pair[0]*pair[1] for pair in zip(v1, v2))) / pi
    if more_than_straight:
        return 360 - ang
    return ang


def main():
    for runway, info in RUNWAYS.iteritems():
        angles = (
            tuple(utils.deg_to_rad(coord) for coord in pt)
            for pt in info if isinstance(pt, tuple)
        )
        print '{}: {}'.format(runway, round(get_heading(info[0], *angles), 3))

if __name__ == '__main__':
    main()
