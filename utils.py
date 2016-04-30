from math import hypot, sin, cos, acos, pi

KERBIN_RADIUS = 600

MAP_WIDTH = 4096
MAP_HEIGHT = 2048
MAP_BASE_LONGITUDE = 60
MAP_LINE_WIDTH = 3
MAP_ARROW_OFFSET = 15
MAP_ARROWHEAD_TAN = 0.25
MAP_ARROWHEAD_LENGTH = 25
MAP_POINT_RADIUS = 0.001 * max(MAP_WIDTH, MAP_HEIGHT)


def deg_to_rad(deg):
    return pi * deg / 180


def point_to_params(pt):
    """Returns point coordinates as a dict for waypoint generator."""
    return [
        ('latitude', pt[0]), ('longitude', pt[1]), ('altitude', pt[2]),
    ]


def point_on_map(pt):
    """Returns the coordinates of point on the map."""
    normalized_x_angle = (pt[1] - MAP_BASE_LONGITUDE) % 360
    return (MAP_WIDTH * normalized_x_angle / 360.0, MAP_HEIGHT * (0.5 - pt[0] / 180.0))


def point_on_sphere(pt):
    """Returns point on a sphere given by angle coordinates."""
    theta, phi = pt
    return (cos(phi) * cos(theta), sin(phi) * cos(theta), sin(theta))


def distance(loc1, loc2):
    """Calculates distance between locations along the surface."""
    loc1 = map(deg_to_rad, loc1.position)
    loc2 = map(deg_to_rad, loc2.position)
    return KERBIN_RADIUS * acos(min(1,
        sin(loc1[0]) * sin(loc2[0]) + cos(loc1[0]) * cos(loc2[0]) * cos(loc1[1] - loc2[1])
    ))


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


def add_arrow(route_map, pt1, pt2, **extra):
    """Adds an arrow from the first point to the second to SVG map."""
    if pt1[0] == pt2[0]:
        # For debug routes from the location to itself.
        return
    if pt1[0] - pt2[0] > MAP_WIDTH / 2:
        two_parts_correction = 1
    elif pt2[0] - pt1[0] > MAP_WIDTH / 2:
        two_parts_correction = -1
    else:
        two_parts_correction = 0
    pt1 = (pt1[0] - two_parts_correction * MAP_WIDTH, pt1[1])

    v = (pt1[0] - pt2[0], pt1[1] - pt2[1])
    norm = MAP_ARROW_OFFSET / hypot(*v)
    pt1 = (pt1[0] - norm * v[0], pt1[1] - norm * v[1])
    pt2 = (pt2[0] + norm * v[0], pt2[1] + norm * v[1])

    norm = MAP_ARROWHEAD_LENGTH / hypot(*v)
    points = [
        pt1, (
            pt2[0] + norm * v[0] + MAP_ARROWHEAD_TAN * norm * v[1],
            pt2[1] + norm * v[1] - MAP_ARROWHEAD_TAN * norm * v[0],
        ), (
            pt2[0] + norm * v[0] - MAP_ARROWHEAD_TAN * norm * v[1],
            pt2[1] + norm * v[1] + MAP_ARROWHEAD_TAN * norm * v[0],
        ),
    ]
    if two_parts_correction:
        route_map.add(route_map.line(
            (pt1[0] + two_parts_correction * MAP_WIDTH, pt1[1]),
            (pt2[0] + two_parts_correction * MAP_WIDTH, pt2[1]),
            **extra
        ))
    for pt in points:
        route_map.add(route_map.line(pt, pt2, **extra))

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
