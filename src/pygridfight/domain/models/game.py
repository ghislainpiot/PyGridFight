"""Game domain model for PyGridFight."""

from typing import Dict, Optional
from pydantic import BaseModel, Field, field_validator, model_validator
from src.pygridfight.domain.models.grid import Grid
from src.pygridfight.domain.models.position import Position
from src.pygridfight.domain.models.player import Player
from src.pygridfight.domain.models.avatar import Avatar
import uuid
from typing import Optional
from pydantic import BaseModel, Field

class GameSettings(BaseModel):
    name: str
    max_players: int
    grid_size: int
    is_private: bool = False

class Game(BaseModel):
    """Game domain model for PyGridFight.

    Attributes:
        id: Unique identifier for the game.
        grid: The game grid.
        players: Dictionary of player_id to Player.
        avatars: Dictionary of avatar_id to Avatar.
        status: Game status ("waiting", "active", "finished").
        turn: Current turn number.
    """

    id: str = Field(..., min_length=1)
    grid: Grid
    players: Dict[str, Player] = Field(default_factory=dict)
    avatars: Dict[str, Avatar] = Field(default_factory=dict)
    status: str = Field(default="waiting", pattern="^(waiting|active|finished)$")
    turn: int = Field(default=0, ge=0)

    # API metadata fields
    name: Optional[str] = None
    max_players: Optional[int] = None
    grid_size: Optional[int] = None
    is_private: Optional[bool] = None

    @field_validator("id")
    @classmethod
    def validate_id(cls, v: str) -> str:
        if not v or not isinstance(v, str):
            raise ValueError("Game id must be a non-empty string")
        return v

    def add_player(self, player: Player) -> None:
        """Add a player to the game.

        Args:
            player: The Player instance to add.

        Raises:
            ValueError: If player already exists.
        """
        if player.id in self.players:
            raise ValueError(f"Player {player.id} already in game")
        self.players[player.id] = player

    def remove_player(self, player_id: str) -> None:
        """Remove a player from the game.

        Args:
            player_id: The ID of the player to remove.
        """
        self.players.pop(player_id, None)
        # Remove all avatars belonging to this player
        to_remove = [aid for aid, av in self.avatars.items() if av.player_id == player_id]
        for aid in to_remove:
            self.avatars.pop(aid, None)

    def create_initial_avatar(self, player_id: str) -> Avatar:
        """Create and place an initial avatar for a player.

        Args:
            player_id: The ID of the player.

        Returns:
            The created Avatar.

        Raises:
            ValueError: If player does not exist or already has an avatar.
        """
        if player_id not in self.players:
            raise ValueError(f"Player {player_id} not found")
        # Only one avatar per player for now (YAGNI)
        for av in self.avatars.values():
            if av.owner_id == player_id:
                raise ValueError(f"Player {player_id} already has an avatar")
        # Place avatar at a default position (top-left, bottom-right, etc.)
        if len(self.players) == 1:
            pos = Position(x=0, y=0)
        elif len(self.players) == 2:
            pos = Position(x=self.grid.width - 1, y=self.grid.height - 1)
        else:
            # For more players, just pick next available corner or (0,0)
            pos = Position(x=0, y=0)
        avatar_id = str(uuid.uuid4())
        avatar = Avatar(id=avatar_id, owner_id=player_id, position=pos.model_dump())
        self.avatars[avatar_id] = avatar
        self.players[player_id].add_avatar(avatar_id)
        return avatar

    def check_victory_conditions(self) -> Optional[str]:
        """Check if any player meets the victory condition.

        Returns:
            The player_id of the winner, or None if no winner.
        """
        # Simplified: first player to reach score >= 10 wins
        for player in self.players.values():
            if getattr(player, "score", 0) >= 10:
                return player.id
        return None

    def get_state(self) -> dict:
        """Get a serializable representation of the game state.

        Returns:
            A dictionary representing the game state.
        """
        return {
            "id": self.id,
            "status": self.status,
            "turn": self.turn,
            "players": {pid: player.model_dump() for pid, player in self.players.items()},
            "avatars": {aid: avatar.model_dump() for aid, avatar in self.avatars.items()},
            "grid": self.grid.model_dump(),
        }