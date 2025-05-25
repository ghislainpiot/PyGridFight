from typing import List, Any
from uuid import UUID

from ..core.models import Coordinates

class Avatar:
    """
    Represents a player's avatar on the grid.

    Attributes:
        avatar_id (UUID): Unique identifier for the avatar.
        player_id (UUID): Unique identifier for the owning player.
        position (Coordinates): Current position of the avatar on the grid.
        active_powerups (List[Any]): List of currently active power-ups (to be refined to ActivePowerUp).
    """

    def __init__(
        self,
        avatar_id: UUID,
        player_id: UUID,
        initial_position: Coordinates,
    ) -> None:
        """
        Initialize an Avatar entity.

        Args:
            avatar_id (UUID): Unique identifier for the avatar.
            player_id (UUID): Unique identifier for the owning player.
            initial_position (Coordinates): Starting position of the avatar.
        """
        self.avatar_id: UUID = avatar_id
        self.player_id: UUID = player_id
        self.position: Coordinates = initial_position
        self.active_powerups: List[Any] = []

    def move(self, new_position: Coordinates) -> None:
        """
        Move the avatar to a new position.

        Args:
            new_position (Coordinates): The new position to move the avatar to.
        """
        self.position = new_position
