import pytest

from pygridfight.core.models import Coordinates

def test_coordinates_initialization():
    """Test that Coordinates initializes with correct x and y values."""
    coord = Coordinates(x=3, y=5)
    assert coord.x == 3
    assert coord.y == 5

def test_coordinates_immutable():
    """Test that Coordinates is immutable (frozen dataclass)."""
    coord = Coordinates(x=1, y=2)
    with pytest.raises(Exception):
        coord.x = 10
    with pytest.raises(Exception):
        coord.y = 20

@pytest.mark.parametrize("x, y", [
    (0, 0),
    (10, -5),
    (-7, 8),
])
def test_coordinates_equality(x, y):
    """Test equality comparison for Coordinates."""
    coord1 = Coordinates(x=x, y=y)
    coord2 = Coordinates(x=x, y=y)
    assert coord1 == coord2
    assert hash(coord1) == hash(coord2)

@pytest.mark.parametrize("x, y", [
    (1.5, 2),
    ("1", 2),
    (1, "2"),
    (None, 2),
    (1, None),
])
def test_coordinates_type_validation(x, y):
    """Test that Coordinates enforces integer types for x and y."""
    with pytest.raises((TypeError, ValueError)):
        Coordinates(x=x, y=y)