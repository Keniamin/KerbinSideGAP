import re
from math import hypot

import geometry

MAP_WIDTH = 4096
MAP_HEIGHT = 2048
MAP_BASE_LONGITUDE = 60
MAP_ARROW_OFFSET = 10  # km
MAP_BEACON_OFFSET = 3  # km

MAP_LINE_WIDTH = 0.0005 * (MAP_WIDTH + MAP_HEIGHT)
MAP_POINT_RADIUS = 0.001 * max(MAP_WIDTH, MAP_HEIGHT)
MAP_CROSS_LINE_WIDTH = 0.5 * MAP_LINE_WIDTH
MAP_CROSS_HALF_LENGTH = 1.5 * MAP_POINT_RADIUS
MAP_FONT_SIZE = MAP_POINT_RADIUS * 8
MAP_ARROWHEAD_LENGTH = 0.01 * min(MAP_WIDTH, MAP_HEIGHT)
MAP_ARROWHEAD_TANGENT = MAP_ARROWHEAD_LENGTH / 3.0
MAP_CYCLE = geometry.Vector(MAP_WIDTH, 0)


def loc_distance(loc1, loc2):
    """Calculates distance between locations along the surface."""
    return geometry.distance(loc1.position, loc2.position)


def point_to_params(pt, absolute_altitude=False):
    """Returns point coordinates as a list for Contract Configurator waypoint."""
    alt =  pt[2].absolute if absolute_altitude else pt[2].relative
    return [
        ('latitude', pt[0]), ('longitude', pt[1]), ('altitude', alt),
    ]


def point_on_map(pt):
    """Returns the coordinates of point on the map."""
    normalized_x_angle = (pt[1] - MAP_BASE_LONGITUDE) % 360
    return geometry.Vector(
        MAP_WIDTH * normalized_x_angle / 360.0,
        MAP_HEIGHT * (0.5 - pt[0] / 180.0),
    )


def write_config(out, node, level=0):
    """Recursively writes config to the out file."""
    lf_align = '\n' + '\t' * level
    for param, value in node:
        if isinstance(value, list):
            out.write(''.join([lf_align, param, lf_align, '{']))
            write_config(out, value, level+1)
            out.write(lf_align + '}')
        else:
            out.write('{}{} = {}'.format(lf_align, param, value))
    if level == 0:
        out.write('\n')


def add_route_arrow(route_map, loc1, loc2, beacons=None, **extra):
    """
    Adds a route arrow to SVG map. The route represents real path on the
    surface from the first location to the second.
    """
    pt1 = loc1.position
    pt2 = loc2.position
    dist = geometry.distance(pt1, pt2)
    if dist < 3 * MAP_ARROW_OFFSET:
        raise ValueError('Too short route {}, can not draw correctly'.format(dist))

    if beacons is None:
        pt1 = geometry.step_to(pt1, pt2, MAP_ARROW_OFFSET)
        pt2 = geometry.step_to(pt2, pt1, MAP_ARROW_OFFSET)
        waypoints = [(False, pt2)]
    else:
        start, takeoff = loc1.runways[0]
        last_beacon_position = beacons[-1][1] if beacons else pt1
        touchdown, stop = select_runway(loc2, last_beacon_position)
        pt1 = geometry.step_to(takeoff, start, -MAP_ARROW_OFFSET)
        pt2 = geometry.step_to(touchdown, stop, -MAP_ARROW_OFFSET)
        waypoints = [(True, beacon) for _, beacon in beacons] + [(False, pt2)]
    path = route_map.path(d=['M'], fill='none', **extra)

    step = None
    prev_waypoint = pt1
    prev_pt = point_on_map(pt1)
    path.push(prev_pt.svg_form())
    for is_beacon, next_waypoint in waypoints:
        if is_beacon:
            prev_vector = geometry.point_on_sphere(prev_waypoint)
            next_vector = geometry.point_on_sphere(next_waypoint)
            offset = next_vector + geometry.Vector.cross(next_vector, prev_vector - next_vector)
            offset_direction = geometry.angles_from_sphere(geometry.Vector.normalize(offset))
            next_waypoint = geometry.step_to(next_waypoint, offset_direction, MAP_BEACON_OFFSET)
        for cur_pt in geometry.make_route_points(prev_waypoint, next_waypoint, include_first=False):
            cur_pt = point_on_map(cur_pt)
            step = cur_pt - prev_pt
            cycle_dir = reference = 0
            if cur_pt[0] > prev_pt[0] + MAP_WIDTH / 2:
                cycle_dir, reference = 1, 0
            elif cur_pt[0] < prev_pt[0] - MAP_WIDTH / 2:
                cycle_dir, reference = -1, MAP_WIDTH
            if cycle_dir:
                step -= MAP_CYCLE * cycle_dir
                extra_part = ((prev_pt + step)[0] - reference) / step[0]
                intermediate_pt = prev_pt + step * (1 - extra_part)
                path.push(intermediate_pt.svg_form())
                intermediate_pt += MAP_CYCLE * cycle_dir
                path.push('M', intermediate_pt.svg_form())
            path.push(cur_pt.svg_form())
            prev_pt = cur_pt
        prev_waypoint = next_waypoint

    last_step_dir = geometry.Vector.normalize(step)
    arrowhead_base = cur_pt - MAP_ARROWHEAD_LENGTH * last_step_dir
    arrowhead_tangent = MAP_ARROWHEAD_TANGENT * geometry.Vector(-last_step_dir[1], last_step_dir[0])
    path.push(
        (arrowhead_base + arrowhead_tangent).svg_form(),
        'M', (arrowhead_base - arrowhead_tangent).svg_form(),
        cur_pt.svg_form(),
    )

    route_map.add(path)


def add_beacon(route_map, pt):
    """Adds a beacon mark to SVG map."""
    path = []
    for cross_leg in [
        geometry.Vector(MAP_CROSS_HALF_LENGTH, MAP_CROSS_HALF_LENGTH),
        geometry.Vector(MAP_CROSS_HALF_LENGTH, -MAP_CROSS_HALF_LENGTH),
    ]:
        path.extend(['M', (pt - cross_leg).svg_form(), (pt + cross_leg).svg_form()])
    route_map.add(route_map.path(
        d=path, fill='none', stroke='black', stroke_width='{}px'.format(MAP_CROSS_LINE_WIDTH),
    ))


def select_runway(loc, approach_pt):
    """Returns best runway of location for approach from the specified point."""
    min_diff = result = None
    for ep1, ep2 in loc.runways:
        for gs_pt, loc_pt in [(ep1, ep2), (ep2, ep1)]:
            if gs_pt[3] is None:
                continue
            rw_hdg = geometry.heading(gs_pt, loc_pt)
            appr_hdg = (geometry.heading(gs_pt, approach_pt) + 180) % 360
            hdg_diff = min(abs(rw_hdg-appr_hdg), 360+rw_hdg-appr_hdg, 360+appr_hdg-rw_hdg)
            if min_diff is None or hdg_diff < min_diff:
                min_diff, result = hdg_diff, (gs_pt, loc_pt)
    return result


def calculate_reward(contract, reward_string, calc_min):
    """
    Function to calculate min or max reward using the reward string from
    contract description. Yes, it's really crazy. Don't blame me, please.
    """
    def Random(first, second):
        func = (min if calc_min else max)
        return func(float(first), float(second))

    if 'needSecondCrewMember' in reward_string:
        reward_string = reward_string.replace('@/needSecondCrewMember', '0' if calc_min else '1')
    if 'passengersNum' in reward_string:
        reward_string = reward_string.replace(
            '@/passengersNum',
            'Random({}, {})'.format(contract.passengers_number[0], contract.passengers_number[1]),
        )

    assert '@/' not in reward_string, 'Some variable is unknown in "{}"'.format(reward_string)
    return int(eval(reward_string))


def normalize_flight_description(description):
    """
    Makes description without variables required by ContractConfigurator at
    pre-generation stage.
    """
    description = re.sub('@/VIK[a-z]*', 'Very Important Kerbal', description)
    assert '@/' not in description, 'Unexpected variable(s) in "{}"'.format(description)
    return description
