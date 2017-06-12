import classes
import geometry
from routes import ROUTES


class TestFlightContract(classes.TouristGroupFlightContract):
    """Describes a test."""
    route_color = 'white'
    weight = 10
    max_simultaneous = 1
    passengers_number = (2, 4)


real_distance = geometry.distance
geometry.distance = lambda *args: max(real_distance(*args), 0.1)

ROUTES[("Kerbal Space Centre", "Kerbal Space Centre")] = TestFlightContract(
    objective="Perform a test.",
    #staff_type="Scientist",
    reward=0,
)
