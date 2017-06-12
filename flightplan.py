from math import tan

import utils
import geometry

METERS_PER_KILOMETER = 1000

ASC_TANG = tan(geometry.deg_to_rad(10.0)) * METERS_PER_KILOMETER
DESC_TANG = tan(geometry.deg_to_rad(10.0)) * METERS_PER_KILOMETER

TAKEOFF_ALTITUDE = 0.1 * ASC_TANG
TAKEOFF_STRAIGHT_UNTIL_ALTITUDE = 1500

MIN_GLIDESLOPE_ANGLE = 3.3
MIN_IAF_LEVEL_DISTANCE = 3.0
IAF_DISTANCE = 25.0
FAF_DISTANCE = 10.0
FLARE_DISTANCE = 0.2

GLIDESLOPE_ALTITUDE_CORRECTION = 75 * tan(geometry.deg_to_rad(MIN_GLIDESLOPE_ANGLE))


def point_to_params(name, pt, alt=None, marker=None):
    """Returns point coordinates as a list for Kramax AutoPilot flight plan."""
    if alt is None:
        alt = pt[2]
    params = [
        ('name', name),
        ('Vertical', 'true'),
        ('lat', pt[0]),
        ('lon', pt[1]),
        ('alt', int(round(alt))),
    ]
    if marker:
        params.append((marker, 'true'))
    return params


def make_landing_pattern(landing_point, opposite_end):
    """Makes waypoints for landing in Kramax AutoPilot format."""
    iaf_point, iaf_alt = _make_glideslope_point(landing_point, opposite_end, IAF_DISTANCE)
    faf_point, faf_alt = _make_glideslope_point(landing_point, opposite_end, FAF_DISTANCE)
    flare_point, flare_alt = _make_glideslope_point(landing_point, opposite_end, FLARE_DISTANCE)
    return [
        point_to_params('IAF', iaf_point, alt=iaf_alt, marker='IAF'),
        point_to_params('FAF', faf_point, alt=faf_alt, marker='FAF'),
        point_to_params('FLARE', flare_point, alt=flare_alt, marker='RW'),
        point_to_params('STOP', opposite_end, marker='Stop'),
    ]


def make_route_waypoints(from_loc, to_loc, flight_level, beacons):
    """Makes all route waypoints in Kramax AutoPilot format."""

    def add_intermediate_points(
        position,
        prev_beacon_name, beacon_name,
        beacon, beacon_alt,
        min_distance=0,
    ):
        """Helper function to add beacon altitude change point."""

        def normalize_beacon_name(name):
            if not name:
                return ''
            if name.endswith('-NDB'):
                return name[:-3]
            return name + '-'

        alt = position[2]
        if alt < beacon_alt:
            slope_name, tang = 'ASC', ASC_TANG
            fl_level_needed = (alt < flight_level and flight_level <= beacon_alt)
        else:
            slope_name, tang = 'DESC', -DESC_TANG
            fl_level_needed = (alt > flight_level and flight_level >= beacon_alt)
        if fl_level_needed:
            name = normalize_beacon_name(prev_beacon_name) + 'FL-{}'.format(slope_name)
            intermediate = geometry.step_to(position, beacon, (flight_level - alt) / tang)
            points.append(point_to_params(name, intermediate, alt=flight_level))
            alt = flight_level
        if beacon_alt != alt:
            name = normalize_beacon_name(beacon_name) + slope_name
            distance = max(min_distance, (beacon_alt - alt) / tang)
            intermediate = geometry.step_to(beacon, position, distance)
            points.append(point_to_params(name, intermediate, alt=alt))

    points = []

    runway = from_loc.runways[0]
    takeoff_asl = runway[1][2]
    points.append(point_to_params('TAKEOFF', runway[1], alt=(takeoff_asl + TAKEOFF_ALTITUDE)))

    position = geometry.step_to(runway[1], runway[0], - TAKEOFF_STRAIGHT_UNTIL_ALTITUDE / ASC_TANG)
    position = position + type(position)([takeoff_asl + TAKEOFF_STRAIGHT_UNTIL_ALTITUDE])
    points.append(point_to_params('ASCENT', position))

    last_beacon_position = beacons[-1][1] if beacons else position
    landing_point, opposite_end = utils.select_runway(to_loc, last_beacon_position)

    iaf_point, iaf_alt = _make_glideslope_point(landing_point, opposite_end, IAF_DISTANCE)
    faf_point, faf_alt = _make_glideslope_point(landing_point, opposite_end, FAF_DISTANCE)
    flare_point, flare_alt = _make_glideslope_point(landing_point, opposite_end, FLARE_DISTANCE)

    beacon_distances = []
    dist_position = runway[1]
    for _, beacon in beacons:
        beacon_distances.append(geometry.distance(dist_position, beacon))
        dist_position = beacon
    beacon_distances.append(geometry.distance(dist_position, landing_point))

    if not beacons:
        asc_dist = (flight_level - position[2] - 0.1) / ASC_TANG
        fake_beacon = geometry.step_to(position, iaf_point, asc_dist)
        beacons = [('FL-ASC', fake_beacon + type(fake_beacon)([0]))]

    prev_beacon_name = None
    for beacon_name, beacon in beacons:
        asc_alt = position[2] + ASC_TANG * geometry.distance(position, beacon)
        desc_alt = position[2] - DESC_TANG * geometry.distance(position, beacon)
        faf_asc_alt = faf_alt + DESC_TANG * geometry.distance(faf_point, beacon)
        beacon_alt = max(beacon[2], desc_alt, min(asc_alt, faf_asc_alt, flight_level))
        if (
            (beacon_alt > position[2] and beacon_alt < asc_alt)
            or (beacon_alt < position[2] and beacon_alt > desc_alt)
        ):
            add_intermediate_points(position, prev_beacon_name, beacon_name, beacon, beacon_alt)
        position = beacon[:2] + type(beacon)([beacon_alt])
        points.append(point_to_params('{}'.format(beacon_name), position))
        prev_beacon_name = beacon_name

    if geometry.distance(position, landing_point) > 1.25 * IAF_DISTANCE:
        desc_alt = position[2] - DESC_TANG * geometry.distance(position, iaf_point)
        iaf_alt = max(desc_alt, min(iaf_alt, flight_level))
        if iaf_alt > desc_alt:
            add_intermediate_points(
                position, prev_beacon_name, 'IAF',
                iaf_point, iaf_alt, min_distance=MIN_IAF_LEVEL_DISTANCE,
            )
        points.append(point_to_params('IAF', iaf_point, alt=iaf_alt, marker='IAF'))
    else:
        points[-1].append(('IAF', 'true'))

    points.append(point_to_params('FAF', faf_point, alt=faf_alt, marker='FAF'))
    points.append(point_to_params('FLARE', flare_point, alt=flare_alt, marker='RW'))
    points.append(point_to_params('STOP', opposite_end, marker='Stop'))
    return points, beacon_distances


def _get_glideslope_tang(landing_point):
    return METERS_PER_KILOMETER * tan(
        geometry.deg_to_rad(max(MIN_GLIDESLOPE_ANGLE, landing_point[3]))
    )


def _make_glideslope_point(landing_point, opposite_end, distance):
    glideslope_tang = _get_glideslope_tang(landing_point)
    alt = landing_point[2] + distance * glideslope_tang + GLIDESLOPE_ALTITUDE_CORRECTION
    point = geometry.step_to(landing_point, opposite_end, -distance)
    return point, alt
