"""Avatar domain model for PyGridFight."""

from pydantic import BaseModel, Field
from pygridfight.domain.models.grid import Position

class Avatar(BaseModel):
    """
    Represents an avatar on the grid.

    Attributes:
        id (str): Unique identifier for the avatar.
        owner_id (str): The player ID who owns this avatar.
        position (Position): The avatar's position on the grid.
        health (int): The avatar's health (default: 1).
        active (bool): Whether the avatar is active (default: True).
    """
    id: str = Field(..., description="Unique identifier for the avatar")
    owner_id: str = Field(..., description="Player ID who owns this avatar")
    position: Position = Field(..., description="Avatar's position on the grid")
    health: int = Field(default=1, ge=0, description="Avatar's health (must be >= 0)")
    active: bool = Field(default=True, description="Whether the avatar is active")

    def is_alive(self) -> bool:
        """
        Check if the avatar is alive (health > 0 and active).

        Returns:
            bool: True if alive, False otherwise.
        """
        return self.active and self.health > 0

    def set_position(self, new_position: Position) -> None:
        """
        Update the avatar's position.

        Args:
            new_position (Position): The new position to set.
        """
        self.position = new_position

    def take_damage(self, amount: int) -> None:
        """
        Reduce the avatar's health by the given amount.

        Args:
            amount (int): Amount of damage to take.
        """
        if amount < 0:
            raise ValueError("Damage amount must be non-negative.")
        self.health = max(0, self.health - amount)
        if self.health == 0:
            self.active = False

    def heal(self, amount: int) -> None:
        """
        Heal the avatar by the given amount (if active).

        Args:
            amount (int): Amount to heal.
        """
        if amount < 0:
            raise ValueError("Heal amount must be non-negative.")
        if self.active:
            self.health += amount