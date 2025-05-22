"""Player domain model for PyGridFight."""

from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field

from pygridfight.domain.enums import PlayerStatus


@dataclass
class PlayerStats:
    """Player statistics model."""

    games_played: int = 0
    games_won: int = 0
    total_score: int = 0

    @property
    def average_score(self) -> float:
        """Calculate average score per game."""
        return self.total_score / self.games_played if self.games_played > 0 else 0.0

    @property
    def win_rate(self) -> float:
        """Calculate win rate percentage."""
        return (self.games_won / self.games_played * 100) if self.games_played > 0 else 0.0


@dataclass
class Player:
    """Player domain model."""

    id: str
    name: str
    status: PlayerStatus = PlayerStatus.OFFLINE
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_seen: Optional[datetime] = None
    current_game_id: Optional[str] = None
    stats: PlayerStats = field(default_factory=PlayerStats)

    def join_game(self, game_id: str) -> None:
        """Join a game."""
        self.current_game_id = game_id
        self.status = PlayerStatus.IN_GAME
        self.last_seen = datetime.utcnow()

    def leave_game(self) -> None:
        """Leave current game."""
        self.current_game_id = None
        self.status = PlayerStatus.ONLINE
        self.last_seen = datetime.utcnow()

    def go_online(self) -> None:
        """Set player status to online."""
        self.status = PlayerStatus.ONLINE
        self.last_seen = datetime.utcnow()

    def go_offline(self) -> None:
        """Set player status to offline."""
        self.status = PlayerStatus.OFFLINE
        self.last_seen = datetime.utcnow()

    def update_stats(self, won: bool, score: int) -> None:
        """Update player statistics after a game."""
        self.stats.games_played += 1
        if won:
            self.stats.games_won += 1
        self.stats.total_score += score