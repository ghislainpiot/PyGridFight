from typing import Dict, Optional
from uuid import UUID, uuid4

from ..gameplay.session import GameSession
from ..gameplay.player import Player
from ..gameplay.grid import Grid
from ..scoring.services import ScoreKeeper
from ..gameplay.avatar import Avatar
from ..core.models import Coordinates
from .exceptions import GameNotFoundError

class GameLifecycleManager:
    """
    Service responsible for managing the lifecycle of game sessions.
    Uses in-memory storage for active sessions.
    """

    _active_sessions: Dict[UUID, GameSession]

    def __init__(self) -> None:
        """Initialize the GameLifecycleManager with an empty session store."""
        self._active_sessions: Dict[UUID, GameSession] = {}

    def create_game_session(
        self, player_display_name: str, grid_size: int, target_score: int
    ) -> GameSession:
        """
        Create a new game session with a single player and initial avatar.

        Args:
            player_display_name (str): The display name for the player.
            grid_size (int): The size of the grid.
            target_score (int): The target score to win the game.

        Returns:
            GameSession: The created game session.
        """
        player_id = uuid4()
        avatar_id = uuid4()
        initial_position = Coordinates(x=0, y=0)
        avatar = Avatar(avatar_id=avatar_id, player_id=player_id, initial_position=initial_position)
        player = Player(player_id=player_id, display_name=player_display_name)
        player.add_avatar(avatar)
        grid = Grid(size=grid_size)
        score_keeper = ScoreKeeper()
        score_keeper.record_score(player.player_id, 0)
        game_session = GameSession(
            player=player,
            grid=grid,
            score_keeper=score_keeper,
            target_score=target_score,
        )
        self._active_sessions[game_session.session_id] = game_session
        return game_session

    def get_game_session(self, session_id: UUID) -> Optional[GameSession]:
        """
        Retrieve a game session by its session ID.

        Args:
            session_id (UUID): The session ID to look up.

        Returns:
            Optional[GameSession]: The game session if found, else None.
        """
        return self._active_sessions.get(session_id)

    def get_game_session_or_raise(self, session_id: UUID) -> GameSession:
        """
        Retrieve a game session by its session ID, or raise if not found.

        Args:
            session_id (UUID): The session ID to look up.

        Returns:
            GameSession: The found game session.

        Raises:
            GameNotFoundError: If the session is not found.
        """
        session = self.get_game_session(session_id)
        if session is None:
            raise GameNotFoundError(f"Game session {session_id} not found.")
        return session
