from __future__ import annotations
from typing import List, Any, Optional
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .player import Player
from uuid import UUID

from ..core.models import Coordinates
from .grid import Grid
from .resources import Resource
from .exceptions import InvalidMoveError

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

    def move(self, new_coordinates: Coordinates, grid: Grid) -> None:
        """
        Move the avatar to a new position, validating with the grid.

        Args:
            new_coordinates (Coordinates): The new position to move the avatar to.
            grid (Grid): The grid to validate the move against.

        Raises:
            InvalidMoveError: If the move is outside grid boundaries or to a non-existent cell.
        """
        if not grid.is_valid_coordinates(new_coordinates):
            raise InvalidMoveError(f"Target coordinates {new_coordinates} are outside grid boundaries.")
        if grid.get_cell(new_coordinates) is None:
            raise InvalidMoveError(f"Target cell at {new_coordinates} does not exist.")
        self.position = new_coordinates

    def collect(self, grid: Grid, player: "Player") -> Optional[Resource]:
        """
        Attempt to collect a resource at the avatar's current position.

        Args:
            grid (Grid): The grid to collect the resource from.
            player (Player): The player owning this avatar, to update currency if collected.

        Returns:
            Optional[Resource]: The collected resource, or None if no resource was present.
        """
        # Import here to avoid circular import

        collected_resource = grid.collect_resource_at(self.position)
        if collected_resource:
            player.update_currency(collected_resource.value)
        return collected_resource
