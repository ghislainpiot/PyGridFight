"""Player domain model for PyGridFight."""

from pydantic import BaseModel, Field


class Player(BaseModel):
    """
    Represents a player in PyGridFight.

    Attributes:
        id (str): Unique identifier for the player.
        display_name (str): Display name for the player.
        score (int): Player's score (default: 0).
        avatar_ids (List[str]): List of avatar IDs owned by the player.
    """

    id: str = Field(..., description="Unique identifier for the player")
    display_name: str = Field(..., description="Display name for the player")
    score: int = Field(default=0, ge=0, description="Player's score (must be >= 0)")
    avatar_ids: list[str] = Field(
        default_factory=list, description="List of avatar IDs owned by the player"
    )

    def add_avatar(self, avatar_id: str) -> None:
        """
        Add an avatar ID to the player's list of avatars.

        Args:
            avatar_id (str): The avatar ID to add.
        """
        if avatar_id not in self.avatar_ids:
            self.avatar_ids.append(avatar_id)

    def remove_avatar(self, avatar_id: str) -> None:
        """
        Remove an avatar ID from the player's list of avatars.

        Args:
            avatar_id (str): The avatar ID to remove.
        """
        if avatar_id in self.avatar_ids:
            self.avatar_ids.remove(avatar_id)

    def increment_score(self, amount: int = 1) -> None:
        """
        Increment the player's score.

        Args:
            amount (int): Amount to increment (default: 1).
        """
        if amount < 0:
            raise ValueError("Score increment must be non-negative.")
        self.score += amount

    def reset_score(self) -> None:
        """
        Reset the player's score to zero.
        """
        self.score = 0
