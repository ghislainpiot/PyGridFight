from dataclasses import dataclass
from typing import Optional
from pygridfight.core.models import Coordinates
from pygridfight.core.enums import ResourceTypeEnum

@dataclass(frozen=True)
class Cell:
    """
    Value object representing a single cell on the grid.

    Attributes:
        coordinates (Coordinates): The coordinates of the cell on the grid.
        resource_type (Optional[ResourceTypeEnum]): The type of resource present in the cell, if any.
    """
    coordinates: Coordinates
    resource_type: Optional[ResourceTypeEnum] = None