"""Player action classes for PyGridFight gameplay."""

from uuid import UUID
from dataclasses import dataclass
from ..core.models import Coordinates

@dataclass(frozen=True)
class MoveAction:
    """
    Represents a move action for an avatar.

    Attributes:
        avatar_id (UUID): The unique identifier of the avatar to move.
        target_coordinates (Coordinates): The coordinates to move the avatar to.
    """
    avatar_id: UUID
    target_coordinates: Coordinates

@dataclass(frozen=True)
class CollectAction:
    """
    Represents a collect action for an avatar.

    Attributes:
        avatar_id (UUID): The unique identifier of the avatar performing the collection.
        target_coordinates (Coordinates): The coordinates from which to collect a resource.
    """
    avatar_id: UUID
    target_coordinates: Coordinates