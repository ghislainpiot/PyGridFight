"""Game domain model for PyGridFight."""

from datetime import datetime
from typing import List, Optional, Dict
from dataclasses import dataclass, field

from pygridfight.domain.enums import GameStatus


@dataclass
class Game:
    """Game domain model."""

    id: str
    name: str
    status: GameStatus = GameStatus.WAITING
    max_players: int = 4
    grid_size: int = 20
    is_private: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    current_turn: Optional[str] = None
    turn_number: int = 0
    player_ids: List[str] = field(default_factory=list)

    def add_player(self, player_id: str) -> None:
        """Add a player to the game."""
        if len(self.player_ids) >= self.max_players:
            raise ValueError("Game is full")
        if player_id not in self.player_ids:
            self.player_ids.append(player_id)

    def remove_player(self, player_id: str) -> None:
        """Remove a player from the game."""
        if player_id in self.player_ids:
            self.player_ids.remove(player_id)

    def start_game(self) -> None:
        """Start the game."""
        if len(self.player_ids) < 2:
            raise ValueError("Need at least 2 players to start")
        self.status = GameStatus.ACTIVE
        self.started_at = datetime.utcnow()
        self.current_turn = self.player_ids[0] if self.player_ids else None

    def end_game(self) -> None:
        """End the game."""
        self.status = GameStatus.FINISHED
        self.finished_at = datetime.utcnow()

    @property
    def current_players(self) -> int:
        """Get current number of players."""
        return len(self.player_ids)

    @property
    def is_full(self) -> bool:
        """Check if game is full."""
        return len(self.player_ids) >= self.max_players