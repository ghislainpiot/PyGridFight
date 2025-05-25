import uuid
from unittest import mock

import pytest

from pygridfight.gameplay.player import Player
from pygridfight.gameplay.grid import Grid
from pygridfight.gameplay.resources import Resource
from pygridfight.scoring.services import ScoreKeeper
from pygridfight.core.enums import GameStatusEnum, ResourceTypeEnum
from pygridfight.core.models import Coordinates

# Import GameSession after implementation, but for TDD, we expect it to exist
try:
    from pygridfight.gameplay.session import GameSession
except ImportError:
    GameSession = None  # For initial red phase

class DummyCell:
    def __init__(self):
        self.resource = None

@pytest.fixture
def player():
    return Player(player_id=uuid.uuid4(), display_name="TestPlayer")

@pytest.fixture
def grid():
    # 3x3 grid for simplicity
    cells = {}
    for x in range(3):
        for y in range(3):
            cells[Coordinates(x, y)] = DummyCell()
    grid = mock.Mock(spec=Grid)
    grid.cells = cells
    def spawn_resource(coord, resource):
        grid.cells[coord].resource = resource
    grid.spawn_resource.side_effect = spawn_resource
    return grid

@pytest.fixture
def score_keeper(player):
    sk = mock.Mock(spec=ScoreKeeper)
    sk.check_victory_condition.return_value = None
    return sk

@pytest.fixture
def session(player, grid, score_keeper):
    # Target score is 5 for tests
    return GameSession(player=player, grid=grid, score_keeper=score_keeper, target_score=5)

def test_initialization(player, grid, score_keeper):
    session = GameSession(player=player, grid=grid, score_keeper=score_keeper, target_score=7)
    assert isinstance(session.session_id, uuid.UUID)
    assert session.player is player
    assert session.grid is grid
    assert session.score_keeper is score_keeper
    assert session.target_score == 7
    assert session.status == GameStatusEnum.LOBBY
    assert session.current_turn == 0
    assert session.winner is None

def test_start_game_changes_status_and_spawns_resources(session):
    with mock.patch.object(session, '_spawn_resources') as mock_spawn:
        session.start_game()
        assert session.status == GameStatusEnum.IN_PROGRESS
        mock_spawn.assert_called_once()

def test_process_turn_increments_turn_and_spawns_resources_and_checks_end(session):
    session.status = GameStatusEnum.IN_PROGRESS
    with mock.patch.object(session, '_spawn_resources') as mock_spawn, \
         mock.patch.object(session, '_check_game_end') as mock_check_end:
        session.process_turn()
        assert session.current_turn == 1
        mock_spawn.assert_called_once()
        mock_check_end.assert_called_once()

def test_process_turn_does_nothing_if_not_in_progress(session):
    session.status = GameStatusEnum.LOBBY
    with mock.patch.object(session, '_spawn_resources') as mock_spawn, \
         mock.patch.object(session, '_check_game_end') as mock_check_end:
        session.process_turn()
        assert session.current_turn == 0
        mock_spawn.assert_not_called()
        mock_check_end.assert_not_called()

def test_resource_spawning_places_resources_on_empty_cells(session, grid):
    # Mark one cell as occupied
    occupied = list(grid.cells.keys())[0]
    grid.cells[occupied].resource = Resource(resource_type=ResourceTypeEnum.CURRENCY, value=1)
    empty_cells = [coord for coord, cell in grid.cells.items() if cell.resource is None]
    # Patch random.sample to control which cells are chosen
    with mock.patch('random.sample', return_value=empty_cells[:session.NUM_RESOURCES_PER_TURN]):
        session._spawn_resources()
    # Check that resources were placed
    for coord in empty_cells[:session.NUM_RESOURCES_PER_TURN]:
        cell = grid.cells[coord]
        assert cell.resource is not None
        assert cell.resource.resource_type == ResourceTypeEnum.CURRENCY
        assert cell.resource.value == session.RESOURCE_VALUE

def test_resource_spawning_handles_few_empty_cells(session, grid):
    # Only one empty cell
    for cell in grid.cells.values():
        cell.resource = Resource(resource_type=ResourceTypeEnum.CURRENCY, value=1)
    last_coord = list(grid.cells.keys())[-1]
    grid.cells[last_coord].resource = None
    with mock.patch('random.sample', return_value=[last_coord]):
        session._spawn_resources()
    assert grid.cells[last_coord].resource is not None

def test_victory_condition_sets_status_and_winner(session, player, score_keeper):
    session.status = GameStatusEnum.IN_PROGRESS
    winner_id = player.player_id
    score_keeper.check_victory_condition.return_value = winner_id
    session._check_game_end()
    assert session.status == GameStatusEnum.FINISHED
    assert session.winner == winner_id

def test_no_victory_condition_leaves_status_in_progress(session, score_keeper):
    session.status = GameStatusEnum.IN_PROGRESS
    score_keeper.check_victory_condition.return_value = None
    session._check_game_end()
    assert session.status == GameStatusEnum.IN_PROGRESS
    assert session.winner is None
from pygridfight.gameplay.actions import MoveAction, CollectAction
from pygridfight.gameplay.exceptions import InvalidMoveError

def make_avatar_with_id(avatar_id, position):
    avatar = mock.Mock()
    avatar.avatar_id = avatar_id
    avatar.position = position
    return avatar

def test_process_player_action_move_valid(session):
    avatar_id = uuid.uuid4()
    avatar = make_avatar_with_id(avatar_id, Coordinates(0, 0))
    session.player.avatars = [avatar]
    action = MoveAction(avatar_id=avatar_id, target_coordinates=Coordinates(1, 1))
    with mock.patch.object(avatar, "move") as mock_move, \
         mock.patch.object(session, "_check_game_end") as mock_check_end:
        session.process_player_action(action)
        mock_move.assert_called_once_with(Coordinates(1, 1), session.grid)
        mock_check_end.assert_called_once()

def test_process_player_action_move_invalid(session, capsys):
    avatar_id = uuid.uuid4()
    avatar = make_avatar_with_id(avatar_id, Coordinates(0, 0))
    session.player.avatars = [avatar]
    action = MoveAction(avatar_id=avatar_id, target_coordinates=Coordinates(1, 1))
    with mock.patch.object(avatar, "move", side_effect=InvalidMoveError("bad move")), \
         mock.patch.object(session, "_check_game_end") as mock_check_end:
        session.process_player_action(action)
        out = capsys.readouterr().out
        assert "Move failed for avatar" in out
        mock_check_end.assert_called_once()

def test_process_player_action_collect_valid_currency(session):
    avatar_id = uuid.uuid4()
    coords = Coordinates(2, 2)
    avatar = make_avatar_with_id(avatar_id, coords)
    session.player.avatars = [avatar]
    action = CollectAction(avatar_id=avatar_id, target_coordinates=coords)
    resource = mock.Mock()
    resource.resource_type = ResourceTypeEnum.CURRENCY
    resource.value = 10
    with mock.patch.object(avatar, "collect", return_value=resource) as mock_collect, \
         mock.patch.object(session.score_keeper, "record_score") as mock_record_score, \
         mock.patch.object(session, "_check_game_end") as mock_check_end:
        session.process_player_action(action)
        mock_collect.assert_called_once_with(session.grid, session.player)
        mock_record_score.assert_called_once_with(session.player.player_id, 10)
        mock_check_end.assert_called_once()

def test_process_player_action_collect_not_at_target(session, capsys):
    avatar_id = uuid.uuid4()
    avatar = make_avatar_with_id(avatar_id, Coordinates(0, 0))
    session.player.avatars = [avatar]
    action = CollectAction(avatar_id=avatar_id, target_coordinates=Coordinates(1, 1))
    with mock.patch.object(session, "_check_game_end") as mock_check_end:
        session.process_player_action(action)
        out = capsys.readouterr().out
        assert "Collect failed: Avatar" in out
        mock_check_end.assert_not_called()

def test_process_player_action_collect_none(session):
    avatar_id = uuid.uuid4()
    coords = Coordinates(2, 2)
    avatar = make_avatar_with_id(avatar_id, coords)
    session.player.avatars = [avatar]
    action = CollectAction(avatar_id=avatar_id, target_coordinates=coords)
    with mock.patch.object(avatar, "collect", return_value=None) as mock_collect, \
         mock.patch.object(session.score_keeper, "record_score") as mock_record_score, \
         mock.patch.object(session, "_check_game_end") as mock_check_end:
        session.process_player_action(action)
        mock_collect.assert_called_once_with(session.grid, session.player)
        mock_record_score.assert_not_called()
        mock_check_end.assert_called_once()

def test_process_player_action_avatar_not_found(session, capsys):
    avatar_id = uuid.uuid4()
    session.player.avatars = []
    action = MoveAction(avatar_id=avatar_id, target_coordinates=Coordinates(1, 1))
    with mock.patch.object(session, "_check_game_end") as mock_check_end:
        session.process_player_action(action)
        out = capsys.readouterr().out
        assert f"Avatar {avatar_id}" in out
        mock_check_end.assert_not_called()