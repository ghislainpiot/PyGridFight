import pytest
from pygridfight.core.models import Coordinates
from pygridfight.gameplay.models import Cell

# Import Grid after implementation; for now, expect ImportError for TDD Red phase
try:
    from pygridfight.gameplay.grid import Grid
except ImportError:
    Grid = None

def test_grid_initialization():
    if Grid is None:
        pytest.skip("Grid not implemented yet")
    size = 8
    grid = Grid(size=size)
    assert grid.size == size
    assert isinstance(grid.cells, dict)
    assert len(grid.cells) == size * size

def test_grid_cells_are_cells_with_correct_coordinates():
    if Grid is None:
        pytest.skip("Grid not implemented yet")
    size = 4
    grid = Grid(size=size)
    for x in range(size):
        for y in range(size):
            coords = Coordinates(x=x, y=y)
            cell = grid.cells[coords]
            assert isinstance(cell, Cell)
            assert cell.coordinates == coords

def test_grid_get_cell_valid_and_invalid():
    if Grid is None:
        pytest.skip("Grid not implemented yet")
    size = 5
    grid = Grid(size=size)
    coords = Coordinates(x=2, y=3)
    cell = grid.get_cell(coords)
    assert isinstance(cell, Cell)
    assert cell.coordinates == coords
    # Out of bounds
    with pytest.raises(ValueError):
        grid.get_cell(Coordinates(x=5, y=0))
    with pytest.raises(ValueError):
        grid.get_cell(Coordinates(x=0, y=5))
    with pytest.raises(ValueError):
        grid.get_cell(Coordinates(x=-1, y=0))
    with pytest.raises(ValueError):
        grid.get_cell(Coordinates(x=0, y=-1))

def test_grid_is_valid_coordinates():
    if Grid is None:
        pytest.skip("Grid not implemented yet")
    size = 3
    grid = Grid(size=size)
    assert grid.is_valid_coordinates(Coordinates(x=0, y=0)) is True
    assert grid.is_valid_coordinates(Coordinates(x=2, y=2)) is True
    assert grid.is_valid_coordinates(Coordinates(x=3, y=0)) is False
    assert grid.is_valid_coordinates(Coordinates(x=0, y=3)) is False
    assert grid.is_valid_coordinates(Coordinates(x=-1, y=0)) is False
    assert grid.is_valid_coordinates(Coordinates(x=0, y=-1)) is False

def test_grid_cells_initial_state():
    if Grid is None:
        pytest.skip("Grid not implemented yet")
    size = 2
    grid = Grid(size=size)
    for cell in grid.cells.values():
        assert cell.resource_type is None