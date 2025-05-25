import pytest
from uuid import uuid4

from pygridfight.game_lifecycle.manager import GameLifecycleManager
from pygridfight.game_lifecycle.exceptions import GameNotFoundError
from pygridfight.gameplay.session import GameSession
from pygridfight.gameplay.player import Player
from pygridfight.gameplay.grid import Grid
from pygridfight.scoring.services import ScoreKeeper
from pygridfight.gameplay.avatar import Avatar
from pygridfight.core.models import Coordinates
from pygridfight.core.enums import GameStatusEnum

def test_create_game_session():
    manager = GameLifecycleManager()
    player_name = "Alice"
    grid_size = 5
    target_score = 10

    session = manager.create_game_session(player_display_name=player_name, grid_size=grid_size, target_score=target_score)

    assert isinstance(session, GameSession)
    assert session.session_id is not None
    assert isinstance(session.player, Player)
    assert session.player.display_name == player_name
    assert isinstance(session.grid, Grid)
    assert session.grid.size == grid_size
    assert isinstance(session.score_keeper, ScoreKeeper)
    assert session.target_score == target_score
    assert session.status == GameStatusEnum.LOBBY

    # Player has one avatar at (0,0)
    avatars = session.player.avatars
    assert len(avatars) == 1
    avatar = avatars[0]
    assert isinstance(avatar, Avatar)
    assert avatar.position == Coordinates(x=0, y=0)

    # Player's initial score is 0
    assert session.score_keeper.get_score(session.player.player_id) == 0

    # Session is stored in manager
    assert session.session_id in manager._active_sessions

def test_get_game_session_found():
    manager = GameLifecycleManager()
    session = manager.create_game_session("Bob", 6, 15)
    found = manager.get_game_session(session.session_id)
    assert found is session

def test_get_game_session_not_found():
    manager = GameLifecycleManager()
    random_id = uuid4()
    assert manager.get_game_session(random_id) is None

def test_get_game_session_or_raise_found():
    manager = GameLifecycleManager()
    session = manager.create_game_session("Carol", 7, 20)
    found = manager.get_game_session_or_raise(session.session_id)
    assert found is session

def test_get_game_session_or_raise_not_found():
    manager = GameLifecycleManager()
    with pytest.raises(GameNotFoundError):
        manager.get_game_session_or_raise(uuid4())