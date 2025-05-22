import os
import logging
import json
import re
from unittest import mock

import pytest

from src.pygridfight.core import config as config_mod
from src.pygridfight.core import logging as logging_mod

@pytest.fixture(autouse=True)
def clear_env(monkeypatch):
    """Clear relevant env vars before each test."""
    for var in list(os.environ):
        if var.startswith("PYGRIDFIGHT_"):
            monkeypatch.delenv(var, raising=False)

def test_game_settings_defaults():
    settings = config_mod.GameSettings()
    assert settings.grid_size == 8
    assert settings.max_players == 4
    assert settings.max_avatars_per_player == 3
    assert settings.avatar_cost == 5
    assert settings.target_score == 20
    assert settings.max_turns == 50

def test_server_settings_defaults():
    settings = config_mod.ServerSettings()
    assert settings.host == "0.0.0.0"
    assert settings.port == 8000
    assert settings.cors_origins == ["*"]
    assert settings.log_level == "INFO"

def test_game_settings_env_override(monkeypatch):
    monkeypatch.setenv("PYGRIDFIGHT_GRID_SIZE", "12")
    monkeypatch.setenv("PYGRIDFIGHT_MAX_PLAYERS", "2")
    settings = config_mod.GameSettings()
    assert settings.grid_size == 12
    assert settings.max_players == 2

def test_server_settings_env_override(monkeypatch):
    monkeypatch.setenv("PYGRIDFIGHT_HOST", "127.0.0.1")
    monkeypatch.setenv("PYGRIDFIGHT_PORT", "9000")
    monkeypatch.setenv("PYGRIDFIGHT_CORS_ORIGINS", '["http://foo.com"]')
    monkeypatch.setenv("PYGRIDFIGHT_LOG_LEVEL", "DEBUG")
    settings = config_mod.ServerSettings()
    assert settings.host == "127.0.0.1"
    assert settings.port == 9000
    assert settings.cors_origins == ["http://foo.com"]
    assert settings.log_level == "DEBUG"

def test_global_settings_instances():
    gs = config_mod.get_game_settings()
    ss = config_mod.get_server_settings()
    assert isinstance(gs, config_mod.GameSettings)
    assert isinstance(ss, config_mod.ServerSettings)

# Logging output tests removed at user request.