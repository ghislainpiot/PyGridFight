"""In-memory game state management for PyGridFight."""

import time
from typing import Optional, Dict, List
import anyio

from src.pygridfight.domain.models.game import Game
from src.pygridfight.core.config import GameSettings

class GameStateManager:
    """Thread-safe, in-memory manager for PyGridFight game state.

    Implements CRUD for games, player connection tracking, and game expiration.
    Singleton pattern ensures global access.
    """

    _instance = None
    _instance_lock = anyio.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance") or cls._instance is None:
            # Use a lock to ensure thread-safe singleton creation
            # (anyio.Lock is async, so we use a trick: only one thread will ever call __new__ at a time)
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, game_timeout: float = 3600.0):
        """Initialize the GameStateManager.

        Args:
            game_timeout: Timeout in seconds for game expiration (default: 1 hour).
        """
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._games: Dict[str, Game] = {}
        self._connections: Dict[str, Dict[str, dict]] = {}
        self._game_timestamps: Dict[str, float] = {}
        self._lock = anyio.Lock()
        self._game_timeout = game_timeout
        self._initialized = True

    async def create_game(self, game_id: str, settings: GameSettings) -> Game:
        """Create a new game with the given ID and settings.

        Args:
            game_id: Unique identifier for the game.
            settings: GameSettings instance.

        Returns:
            The created Game instance.
        """
        from src.pygridfight.domain.models.grid import Grid  # Local import to avoid circular
        async with self._lock:
            if game_id in self._games:
                raise ValueError(f"Game {game_id} already exists")
            grid = Grid(width=settings.grid_size, height=settings.grid_size)
            game = Game(
                id=game_id,
                grid=grid,
                players={},
                avatars={},
                status="waiting",
                turn=0,
            )
            self._games[game_id] = game
            self._game_timestamps[game_id] = time.monotonic()
            return game

    async def get_game(self, game_id: str) -> Optional[Game]:
        """Retrieve a game by its ID.

        Args:
            game_id: Unique identifier for the game.

        Returns:
            The Game instance if found, else None.
        """
        async with self._lock:
            return self._games.get(game_id)

    async def update_game(self, game_id: str, game: Game) -> None:
        """Update the game state for a given game ID.

        Args:
            game_id: Unique identifier for the game.
            game: The updated Game instance.
        """
        async with self._lock:
            if game_id not in self._games:
                raise ValueError(f"Game {game_id} does not exist")
            self._games[game_id] = game
            self._game_timestamps[game_id] = time.monotonic()

    async def delete_game(self, game_id: str) -> bool:
        """Delete a game by its ID.

        Args:
            game_id: Unique identifier for the game.

        Returns:
            True if the game was deleted, False if not found.
        """
        async with self._lock:
            existed = game_id in self._games
            self._games.pop(game_id, None)
            self._connections.pop(game_id, None)
            self._game_timestamps.pop(game_id, None)
            return existed

    async def list_active_games(self) -> List[str]:
        """List all currently active game IDs.

        Returns:
            List of active game IDs.
        """
        async with self._lock:
            return list(self._games.keys())

    async def add_player_connection(self, game_id: str, player_id: str, connection_info: dict) -> None:
        """Track a player's connection to a game.

        Args:
            game_id: Game ID.
            player_id: Player ID.
            connection_info: Arbitrary connection info (e.g., WebSocket object).
        """
        async with self._lock:
            if game_id not in self._connections:
                self._connections[game_id] = {}
            self._connections[game_id][player_id] = connection_info

    async def remove_player_connection(self, game_id: str, player_id: str) -> None:
        """Remove a player's connection from a game.

        Args:
            game_id: Game ID.
            player_id: Player ID.
        """
        async with self._lock:
            if game_id in self._connections:
                self._connections[game_id].pop(player_id, None)
                if not self._connections[game_id]:
                    self._connections.pop(game_id, None)

    async def get_player_connections(self, game_id: str) -> Dict[str, dict]:
        """Get all player connections for a game.

        Args:
            game_id: Game ID.

        Returns:
            Dict mapping player_id to connection_info.
        """
        async with self._lock:
            return dict(self._connections.get(game_id, {}))

    async def cleanup_expired_games(self) -> None:
        """Remove games that have expired based on the configured timeout."""
        now = time.monotonic()
        async with self._lock:
            expired = [
                gid for gid, ts in self._game_timestamps.items()
                if now - ts > self._game_timeout
            ]
            for gid in expired:
                self._games.pop(gid, None)
                self._connections.pop(gid, None)
                self._game_timestamps.pop(gid, None)

    def reset(self) -> None:
        """Reset all in-memory state (for testing only)."""
        self._games.clear()
        self._connections.clear()
        self._game_timestamps.clear()