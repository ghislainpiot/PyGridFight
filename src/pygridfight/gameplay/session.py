import uuid
import random
from typing import Optional, Union

from ..gameplay.player import Player
from ..gameplay.grid import Grid
from ..gameplay.resources import Resource
from ..scoring.services import ScoreKeeper
from ..core.enums import GameStatusEnum, ResourceTypeEnum
from ..core.models import Coordinates
from .actions import MoveAction, CollectAction
from .exceptions import InvalidMoveError

class GameSession:
    """
    Aggregate root for gameplay. Manages the game state, player, grid, and rules for a single-player session.
    Handles turn processing, resource spawning, and victory condition checking.
    """

    NUM_RESOURCES_PER_TURN: int = 2
    RESOURCE_VALUE: int = 1

    def __init__(
        self,
        player: Player,
        grid: Grid,
        score_keeper: ScoreKeeper,
        target_score: int,
    ) -> None:
        """
        Initialize a new GameSession.

        Args:
            player (Player): The player participating in the session.
            grid (Grid): The game grid.
            score_keeper (ScoreKeeper): The score keeper service.
            target_score (int): The score required for victory.
        """
        self.session_id: uuid.UUID = uuid.uuid4()
        self.player: Player = player
        self.grid: Grid = grid
        self.score_keeper: ScoreKeeper = score_keeper
        self.target_score: int = target_score
        self.status: GameStatusEnum = GameStatusEnum.LOBBY
        self.current_turn: int = 0
        self.winner: Optional[uuid.UUID] = None

    def start_game(self) -> None:
        """
        Start the game session. Sets status to IN_PROGRESS and performs initial resource spawn.
        """
        self.status = GameStatusEnum.IN_PROGRESS
        self._spawn_resources()

    def process_turn(self) -> None:
        """
        Process a single turn for the player.
        Increments the turn counter, spawns resources, and checks for game end.
        """
        if self.status != GameStatusEnum.IN_PROGRESS:
            return
        self.current_turn += 1
        self._spawn_resources()
        self._check_game_end()

    def _spawn_resources(self) -> None:
        """
        Spawn up to NUM_RESOURCES_PER_TURN currency resources at random empty locations on the grid.
        """
        # Find all empty cells (where cell.resource is None)
        empty_coords = [
            coord for coord, cell in self.grid.cells.items() if getattr(cell, "resource", None) is None
        ]
        num_to_spawn = min(self.NUM_RESOURCES_PER_TURN, len(empty_coords))
        if num_to_spawn == 0:
            return
        # Choose random empty cells to spawn resources
        chosen_coords = (
            random.sample(empty_coords, num_to_spawn)
            if len(empty_coords) >= num_to_spawn
            else empty_coords
        )
        for coord in chosen_coords:
            resource = Resource(
                resource_type=ResourceTypeEnum.CURRENCY,
                value=self.RESOURCE_VALUE,
            )
            self.grid.spawn_resource(coord, resource)

    def _check_game_end(self) -> None:
        """
        Check if the victory condition is met. If so, set status to FINISHED and record the winner.
        """
        winner_id = self.score_keeper.check_victory_condition(self.target_score)
        if winner_id is not None:
            self.status = GameStatusEnum.FINISHED
            self.winner = winner_id

    def process_player_action(self, action: Union[MoveAction, CollectAction]) -> None:
        """
        Process a player action (Move or Collect) for the current session.

        Args:
            action (MoveAction or CollectAction): The action to process.
        """
        avatar_to_act = None
        for avatar_obj in self.player.avatars:
            if avatar_obj.avatar_id == action.avatar_id:
                avatar_to_act = avatar_obj
                break
        if avatar_to_act is None:
            print(f"Warning: Avatar {action.avatar_id} not found for player {self.player.player_id}")
            return

        if isinstance(action, MoveAction):
            try:
                avatar_to_act.move(action.target_coordinates, self.grid)
            except InvalidMoveError as e:
                print(f"Move failed for avatar {avatar_to_act.avatar_id}: {e}")
            self._check_game_end()
            return

        if isinstance(action, CollectAction):
            if avatar_to_act.position != action.target_coordinates:
                print(f"Collect failed: Avatar {avatar_to_act.avatar_id} not at target {action.target_coordinates}.")
                return
            collected_resource = avatar_to_act.collect(self.grid, self.player)
            if collected_resource and collected_resource.resource_type == ResourceTypeEnum.CURRENCY:
                self.score_keeper.record_score(self.player.player_id, collected_resource.value)
            self._check_game_end()
