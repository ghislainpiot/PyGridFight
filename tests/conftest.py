"""Pytest configuration and fixtures for PyGridFight tests."""

import pytest
from fastapi.testclient import TestClient

from pygridfight.main import create_app


@pytest.fixture
def app():
    """Create FastAPI app for testing."""
    return create_app()


@pytest.fixture
def client(app):
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def sample_game_data():
    """Sample game data for testing."""
    return {
        "name": "Test Game",
        "max_players": 4,
        "grid_size": 20,
        "is_private": False
    }


@pytest.fixture
def sample_player_data():
    """Sample player data for testing."""
    return {
        "name": "Test Player"
    }