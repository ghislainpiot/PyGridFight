"""Game manager service for PyGridFight."""

from typing import Dict, List, Optional
import uuid

from pygridfight.domain.models.game import Game
from pygridfight.domain.enums import GameStatus
from pygridfight.core.exceptions import GameNotFoundError, GameFullError


class GameManager:
    """Manages game instances and operations."""

    def __init__(self) -> None:
        self._games: Dict[str, Game] = {}

    def create_game(
        self,
        name: str,
        max_players: int = 4,
        grid_size: int = 20,
        is_private: bool = False
    ) -> Game:
        """Create a new game."""
        game_id = str(uuid.uuid4())
        game = Game(
            id=game_id,
            name=name,
            max_players=max_players,
            grid_size=grid_size,
            is_private=is_private
        )
        self._games[game_id] = game
        return game

    def get_game(self, game_id: str) -> Game:
        """Get game by ID."""
        if game_id not in self._games:
            raise GameNotFoundError(game_id)
        return self._games[game_id]

    def list_games(self, include_private: bool = False) -> List[Game]:
        """List all available games."""
        games = []
        for game in self._games.values():
            if not game.is_private or include_private:
                games.append(game)
        return games

    def join_game(self, game_id: str, player_id: str) -> Game:
        """Add player to game."""
        game = self.get_game(game_id)

        if game.is_full:
            raise GameFullError(game_id)

        game.add_player(player_id)
        return game

    def leave_game(self, game_id: str, player_id: str) -> Game:
        """Remove player from game."""
        game = self.get_game(game_id)
        game.remove_player(player_id)

        # Clean up empty games
        if not game.player_ids and game.status == GameStatus.WAITING:
            del self._games[game_id]

        return game

    def start_game(self, game_id: str) -> Game:
        """Start a game."""
        game = self.get_game(game_id)
        game.start_game()
        return game

    def end_game(self, game_id: str) -> Game:
        """End a game."""
        game = self.get_game(game_id)
        game.end_game()
        return game

    def delete_game(self, game_id: str) -> None:
        """Delete a game."""
        if game_id in self._games:
            del self._games[game_id]

    def get_games_count(self) -> int:
        """Get total number of games."""
        return len(self._games)

    def get_active_games(self) -> List[Game]:
        """Get all active games."""
        return [game for game in self._games.values() if game.status == GameStatus.ACTIVE]

    def get_waiting_games(self) -> List[Game]:
        """Get all games waiting for players."""
        return [game for game in self._games.values() if game.status == GameStatus.WAITING]