from dataclasses import dataclass
from pygridfight.core.enums import ResourceTypeEnum

@dataclass(frozen=True)
class Resource:
    """
    Value Object representing a resource on the grid.

    Attributes:
        resource_type: The type of the resource (e.g., ENERGY, GOLD).
        value: The value or amount of the resource.
    """
    resource_type: ResourceTypeEnum
    value: int
