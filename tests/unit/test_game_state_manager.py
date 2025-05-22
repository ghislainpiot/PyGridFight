import asyncio

import anyio
import pytest

from src.pygridfight.core.config import GameSettings
from src.pygridfight.domain.models.game import Game
from src.pygridfight.infrastructure.game_state import GameStateManager


@pytest.fixture
def game_settings():
    return GameSettings(
        grid_size=6,
        max_players=2,
        max_avatars_per_player=1,
        avatar_cost=3,
        target_score=10,
        max_turns=20,
    )


@pytest.fixture
def game_id():
    return "test-game-1"


@pytest.fixture
def player_id():
    return "player-1"


@pytest.fixture
def connection_info():
    return {"ws": "fake-connection-object"}


@pytest.mark.anyio
async def test_singleton_behavior():
    mgr1 = GameStateManager()
    mgr2 = GameStateManager()
    assert mgr1 is mgr2


@pytest.mark.anyio
async def test_create_and_get_game(game_id, game_settings):
    GameStateManager().reset()
    mgr = GameStateManager()
    game = await mgr.create_game(game_id, game_settings)
    assert isinstance(game, Game)
    fetched = await mgr.get_game(game_id)
    assert fetched is not None
    assert fetched.id == game_id


@pytest.mark.anyio
async def test_update_game(game_id, game_settings):
    GameStateManager().reset()
    mgr = GameStateManager()
    game = await mgr.create_game(game_id, game_settings)
    game.status = "active"
    await mgr.update_game(game_id, game)
    updated = await mgr.get_game(game_id)
    assert updated.status == "active"


@pytest.mark.anyio
async def test_delete_game(game_id, game_settings):
    GameStateManager().reset()
    mgr = GameStateManager()
    await mgr.create_game(game_id, game_settings)
    deleted = await mgr.delete_game(game_id)
    assert deleted is True
    assert await mgr.get_game(game_id) is None


@pytest.mark.anyio
async def test_list_active_games(game_settings):
    GameStateManager().reset()
    mgr = GameStateManager()
    await mgr.create_game("g1", game_settings)
    await mgr.create_game("g2", game_settings)
    games = await mgr.list_active_games()
    assert set(games) >= {"g1", "g2"}


@pytest.mark.anyio
async def test_player_connection_tracking(
    game_id, player_id, connection_info, game_settings
):
    GameStateManager().reset()
    mgr = GameStateManager()
    await mgr.create_game(game_id, game_settings)
    await mgr.add_player_connection(game_id, player_id, connection_info)
    conns = await mgr.get_player_connections(game_id)
    assert player_id in conns
    assert conns[player_id] == connection_info
    await mgr.remove_player_connection(game_id, player_id)
    conns = await mgr.get_player_connections(game_id)
    assert player_id not in conns


@pytest.mark.anyio
async def test_game_expiration_cleanup(game_settings):
    GameStateManager().reset()
    mgr = GameStateManager()
    mgr._game_timeout = 0.1
    await mgr.create_game("expiring", game_settings)
    await anyio.sleep(0.2)
    await mgr.cleanup_expired_games()
    assert await mgr.get_game("expiring") is None


@pytest.mark.anyio
async def test_thread_safety_concurrent_create_and_get(game_settings):
    GameStateManager().reset()
    mgr = GameStateManager()

    async def create_and_get(idx):
        gid = f"concurrent-{idx}"
        await mgr.create_game(gid, game_settings)
        return await mgr.get_game(gid)

    results = await asyncio.gather(*[create_and_get(i) for i in range(10)])
    assert all(isinstance(g, Game) for g in results)
