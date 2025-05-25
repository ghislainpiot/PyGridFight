from dataclasses import dataclass
from typing import Optional
from pygridfight.core.models import Coordinates
from pygridfight.gameplay.resources import Resource

@dataclass(frozen=True)
class Cell:
    """
    Value object representing a single cell on the grid.

    Attributes:
        coordinates (Coordinates): The coordinates of the cell on the grid.
        resource (Optional[Resource]): The resource present in the cell, if any.
    """
    coordinates: Coordinates
    resource: Optional[Resource] = None