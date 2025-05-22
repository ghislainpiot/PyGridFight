import pytest
from pydantic import ValidationError

from src.pygridfight.domain.models.grid import Grid, Position


class TestPosition:
    def test_valid_position_creation(self):
        pos = Position(x=3, y=5)
        assert pos.x == 3
        assert pos.y == 5

    @pytest.mark.parametrize(
        "x, y",
        [
            ("a", 1),
            (1, "b"),
            (1.5, 2),
            (2, 1.5),
            (None, 2),
            (2, None),
        ],
    )
    def test_invalid_position_types(self, x, y):
        with pytest.raises(ValidationError):
            Position(x=x, y=y)

    @pytest.mark.parametrize(
        "x, y",
        [
            (-1, 0),
            (0, -1),
            (-5, -5),
        ],
    )
    def test_negative_coordinates_allowed(self, x, y):
        # Negative coordinates are allowed unless otherwise specified
        pos = Position(x=x, y=y)
        assert pos.x == x
        assert pos.y == y


class TestGrid:
    def test_grid_creation(self):
        grid = Grid(width=10, height=8)
        assert grid.width == 10
        assert grid.height == 8

    @pytest.mark.parametrize(
        "width, height",
        [
            (0, 5),
            (5, 0),
            (-1, 5),
            (5, -1),
        ],
    )
    def test_invalid_grid_dimensions(self, width, height):
        with pytest.raises(ValidationError):
            Grid(width=width, height=height)

    @pytest.mark.parametrize(
        "grid_size, pos, expected",
        [
            ((5, 5), Position(x=0, y=0), True),
            ((5, 5), Position(x=4, y=4), True),
            ((5, 5), Position(x=5, y=0), False),
            ((5, 5), Position(x=0, y=5), False),
            ((5, 5), Position(x=-1, y=0), False),
            ((5, 5), Position(x=0, y=-1), False),
        ],
    )
    def test_is_valid_position(self, grid_size, pos, expected):
        grid = Grid(width=grid_size[0], height=grid_size[1])
        assert grid.is_valid_position(pos) is expected

    @pytest.mark.parametrize(
        "grid_size, pos, expected",
        [
            # Center
            (
                (3, 3),
                Position(x=1, y=1),
                [
                    Position(x=0, y=1),
                    Position(x=2, y=1),
                    Position(x=1, y=0),
                    Position(x=1, y=2),
                ],
            ),
            # Corner (0,0)
            (
                (3, 3),
                Position(x=0, y=0),
                [
                    Position(x=1, y=0),
                    Position(x=0, y=1),
                ],
            ),
            # Edge (0,1)
            (
                (3, 3),
                Position(x=0, y=1),
                [
                    Position(x=1, y=1),
                    Position(x=0, y=0),
                    Position(x=0, y=2),
                ],
            ),
            # Edge (2,1)
            (
                (3, 3),
                Position(x=2, y=1),
                [
                    Position(x=1, y=1),
                    Position(x=2, y=0),
                    Position(x=2, y=2),
                ],
            ),
        ],
    )
    def test_get_adjacent_positions(self, grid_size, pos, expected):
        grid = Grid(width=grid_size[0], height=grid_size[1])
        adj = grid.get_adjacent_positions(pos)
        assert set(adj) == set(expected)

    @pytest.mark.parametrize(
        "pos1, pos2, expected",
        [
            (Position(x=0, y=0), Position(x=0, y=0), 0),
            (Position(x=0, y=0), Position(x=1, y=0), 1),
            (Position(x=0, y=0), Position(x=0, y=1), 1),
            (Position(x=0, y=0), Position(x=1, y=1), 2),
            (Position(x=2, y=3), Position(x=5, y=7), 7),
        ],
    )
    def test_distance(self, pos1, pos2, expected):
        assert Grid.distance(pos1, pos2) == expected
