from math import sqrt, sin, cos, tan, asin, acos, pi

KERBIN_RADIUS = 600.0
MAX_ROUTE_STEP = 25.0


class Vector(object):
    DIMENSION_ERROR = 'Can not combine Vectors with different dimensions'

    @classmethod
    def cross(cls, fst, sec):
        assert len(fst) == len(sec), Vector.DIMENSION_ERROR
        if len(fst) == 2:
            return (fst[0] * sec[1] - sec[0] * fst[1])
        if len(fst) == 3:
            return cls(
                fst[1] * sec[2] - sec[1] * fst[2],
                fst[2] * sec[0] - sec[2] * fst[0],
                fst[0] * sec[1] - sec[0] * fst[1],
            )
        raise NotImplementedError

    @classmethod
    def normalize(cls, obj):
        normalizator = 1.0 / abs(obj)
        return cls(coord * normalizator for coord in obj)

    def __init__(self, *args):
        if len(args) == 1:
            args = list(args[0])
        self.data = tuple(args)

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, key):
        return self.data[key]

    def __eq__(self, other):
        return self.data == other.data

    def __add__(self, other):
        if isinstance(other, self.__class__):
            assert len(self) == len(other), Vector.DIMENSION_ERROR
            return self.__class__(pair[0] + pair[1] for pair in zip(self, other))
        raise NotImplementedError

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            assert len(self) == len(other), Vector.DIMENSION_ERROR
            return sum(pair[0] * pair[1] for pair in zip(self, other))
        return self.__class__(coord * other for coord in self)

    def __neg__(self):
        return self * -1

    def __sub__(self, other):
        return self + (-other)

    def __rmul__(self, other):
        return self * other

    def __abs__(self):
        return sqrt(self * self)

    def __repr__(self):
        return self.__class__.__name__ + repr(self.data)

    def svg_form(self):
        return ','.join(str(round(coord, 2)) for coord in self.data)


def deg_to_rad(deg):
    return pi * deg / 180


def rad_to_deg(rad):
    return 180 * rad / pi


def bound(func, arg):
    """Applies arc function (acos or asin) with correct bounds."""
    return func(max(-1, min(1, arg)))


def point_on_sphere(pt):
    """Returns point on a sphere given by angle coordinates."""
    theta, phi = map(deg_to_rad, pt[:2])
    return Vector(cos(phi) * cos(theta), sin(phi) * cos(theta), sin(theta))


def angles_from_sphere(pt):
    """Returns angle coordinates of the point on a sphere."""
    theta = bound(asin, pt[2])
    phi = bound(acos, pt[0] / cos(theta))
    if pt[1] * cos(theta) < 0:
        phi = -phi
    return map(rad_to_deg, (theta, phi))


def chord_to_tangent(pt1, pt2):
    """
    Returns the tangent vector for sphere in the direction of the given chord.
    """
    chord = pt2 - pt1
    coef = chord * pt1
    tang_dir = chord - coef * pt1
    return Vector.normalize(tang_dir)


def step_to(pt1, pt2, dist):
    """
    Returns point lying on the line along the surface from the first point to
    the second, with specified distance from the first point (in kilometres).
    """
    pt1 = point_on_sphere(pt1)
    pt2 = point_on_sphere(pt2)
    if abs(dist) + MAX_ROUTE_STEP > KERBIN_RADIUS * pi / 2:
        raise ValueError(
            'Too big distance {}, can not provide acceptable accuracy'.format(dist)
            + ' (consider dividing step into several parts)'
        )
    tang_distance = tan(dist / KERBIN_RADIUS)
    pt = Vector.normalize(pt1 + chord_to_tangent(pt1, pt2) * tang_distance)
    return angles_from_sphere(pt)


def distance(pt1, pt2):
    """Calculates distance between points along the surface."""
    pt1 = map(deg_to_rad, pt1[:2])
    pt2 = map(deg_to_rad, pt2[:2])
    ang_cos = sin(pt1[0]) * sin(pt2[0]) + cos(pt1[0]) * cos(pt2[0]) * cos(pt1[1] - pt2[1])
    return KERBIN_RADIUS * bound(acos, ang_cos)


def make_route_points(pt1, pt2, include_first=True, include_last=True):
    """
    Yields evenly distributed points lying not too far from each other on the
    line along the surface from the first point to the second.
    """
    dist = distance(pt1, pt2)
    steps = int(dist / MAX_ROUTE_STEP + 0.95)
    step = dist / steps

    if include_first:
        yield pt1
    for _ in xrange(steps - 1):
        pt1 = step_to(pt1, pt2, step)
        yield pt1
    if include_last:
        yield pt2


def heading(pt1, pt2):
    """
    Returns heading at the first point of the direction from the first point to
    the second.
    """
    pt1 = point_on_sphere(pt1)
    pt2 = point_on_sphere(pt2)
    dir_tang = chord_to_tangent(pt1, pt2)
    north_pole = point_on_sphere((90, 0))
    pole_tang = chord_to_tangent(pt1, north_pole)

    heading = rad_to_deg(bound(acos, dir_tang * pole_tang))
    if pt1 * Vector.cross(dir_tang, pole_tang) < 0:
        return 360 - heading
    return heading
