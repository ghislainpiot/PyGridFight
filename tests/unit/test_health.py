"""Basic health check test to verify pytest is working."""

import pytest


def test_basic_assertion():
    """Test that basic assertions work."""
    assert True


def test_health_endpoint(client):
    """Test the health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "pygridfight"


def test_game_manager_creation():
    """Test that GameManager can be created."""
    from pygridfight.services.game_manager import GameManager

    manager = GameManager()
    assert manager is not None
    assert manager.get_games_count() == 0


def test_domain_models():
    """Test that domain models can be imported and created."""
    from pygridfight.domain.models.game import Game
    from pygridfight.domain.models.player import Player
    from pygridfight.domain.enums import GameStatus, PlayerStatus

    # Test Game model
    game = Game(id="test-id", name="Test Game")
    assert game.id == "test-id"
    assert game.name == "Test Game"
    assert game.status == GameStatus.WAITING

    # Test Player model
    player = Player(id="player-id", name="Test Player")
    assert player.id == "player-id"
    assert player.name == "Test Player"
    assert player.status == PlayerStatus.OFFLINE