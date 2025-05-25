import pytest
from pygridfight.core.models import Coordinates
from pygridfight.core.enums import ResourceTypeEnum

# Import Cell after implementation; for now, expect ImportError for TDD Red phase
try:
    from pygridfight.gameplay.models import Cell
except ImportError:
    Cell = None

def test_cell_initialization():
    if Cell is None:
        pytest.skip("Cell not implemented yet")
    coords = Coordinates(x=1, y=2)
    cell = Cell(coordinates=coords, resource_type=ResourceTypeEnum.CURRENCY)
    assert cell.coordinates == coords
    assert cell.resource_type == ResourceTypeEnum.CURRENCY

def test_cell_default_resource_type():
    if Cell is None:
        pytest.skip("Cell not implemented yet")
    coords = Coordinates(x=0, y=0)
    cell = Cell(coordinates=coords)
    assert cell.resource_type is None

def test_cell_immutable():
    if Cell is None:
        pytest.skip("Cell not implemented yet")
    coords = Coordinates(x=0, y=0)
    cell = Cell(coordinates=coords)
    with pytest.raises(Exception):
        cell.coordinates = Coordinates(x=1, y=1)
    with pytest.raises(Exception):
        cell.resource_type = ResourceTypeEnum.WOOD

def test_cell_equality():
    if Cell is None:
        pytest.skip("Cell not implemented yet")
    coords1 = Coordinates(x=1, y=1)
    coords2 = Coordinates(x=1, y=1)
    cell1 = Cell(coordinates=coords1)
    cell2 = Cell(coordinates=coords2)
    assert cell1 == cell2
    cell3 = Cell(coordinates=coords1, resource_type=ResourceTypeEnum.CURRENCY)
    assert cell1 != cell3