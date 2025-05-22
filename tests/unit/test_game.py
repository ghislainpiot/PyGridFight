import pytest
from src.pygridfight.domain.models.game import Game
from src.pygridfight.domain.models.player import Player
from src.pygridfight.domain.models.avatar import Avatar
from src.pygridfight.domain.models.grid import Grid, Position

@pytest.fixture
def sample_grid():
    return Grid(width=4, height=4)

@pytest.fixture
def sample_player():
    return Player(id="p1", display_name="Player One", score=0, avatars=[])

@pytest.fixture
def another_player():
    return Player(id="p2", display_name="Player Two", score=0, avatars=[])

@pytest.fixture
def game(sample_grid):
    return Game(
        id="game-1",
        grid=sample_grid,
        players={},
        avatars={},
        status="waiting",
        turn=0
    )

def test_game_creation(game):
    assert game.id == "game-1"
    assert game.grid.width == 4
    assert game.status == "waiting"
    assert game.turn == 0
    assert isinstance(game.players, dict)
    assert isinstance(game.avatars, dict)

def test_add_and_remove_player(game, sample_player):
    game.add_player(sample_player)
    assert "p1" in game.players
    assert game.players["p1"].display_name == "Player One"
    game.remove_player("p1")
    assert "p1" not in game.players

def test_create_initial_avatar(game, sample_player):
    game.add_player(sample_player)
    avatar = game.create_initial_avatar("p1")
    assert isinstance(avatar, Avatar)
    assert avatar.owner_id == "p1"
    assert avatar.id in game.avatars
    assert avatar.position is not None

def test_get_state(game, sample_player):
    game.add_player(sample_player)
    avatar = game.create_initial_avatar("p1")
    state = game.get_state()
    assert state["id"] == "game-1"
    assert state["status"] == "waiting"
    assert "p1" in state["players"]
    assert avatar.id in state["avatars"]

def test_check_victory_conditions(game, sample_player, another_player):
    game.add_player(sample_player)
    game.add_player(another_player)
    # Simulate a win for p1
    game.players["p1"].score = 10
    game.players["p2"].score = 5
    # Assume victory condition is score >= 10
    result = game.check_victory_conditions()
    assert result == "p1"
    # No winner if no one meets the condition
    game.players["p1"].score = 5
    result = game.check_victory_conditions()
    assert result is None