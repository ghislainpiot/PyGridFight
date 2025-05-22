"""Configuration management for PyGridFight."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class GameSettings(BaseSettings):
    """Game-related settings."""

    grid_size: int = Field(default=8, description="Grid size for the battlefield")
    max_players: int = Field(default=4, description="Maximum number of players")
    max_avatars_per_player: int = Field(default=3, description="Max avatars per player")
    avatar_cost: int = Field(default=5, description="Cost to deploy an avatar")
    target_score: int = Field(default=20, description="Score needed to win")
    max_turns: int = Field(default=50, description="Maximum number of turns per game")

    class Config:
        env_prefix = "PYGRIDFIGHT_"
        case_sensitive = False


class ServerSettings(BaseSettings):
    """Server and API related settings."""

    host: str = Field(default="0.0.0.0", description="Host to bind the server to")
    port: int = Field(default=8000, description="Port to bind the server to")
    cors_origins: list[str] = Field(
        default_factory=lambda: ["*"], description="Allowed CORS origins"
    )
    log_level: str = Field(default="INFO", description="Logging level")

    class Config:
        env_prefix = "PYGRIDFIGHT_"
        case_sensitive = False


@lru_cache
def get_game_settings() -> GameSettings:
    """Get cached game settings."""
    return GameSettings()


@lru_cache
def get_server_settings() -> ServerSettings:
    """Get cached server settings."""
    return ServerSettings()


def get_settings():
    """[DEPRECATED] Compatibility shim. Use get_game_settings() or get_server_settings() instead."""
    # Compose a dummy object with legacy attributes for backward compatibility
    gs = get_game_settings()
    ss = get_server_settings()

    class LegacySettings:
        # Server
        host = ss.host
        port = ss.port
        log_level = ss.log_level
        log_format = getattr(ss, "log_format", "json")
        # CORS
        allowed_origins = getattr(ss, "cors_origins", ["*"])
        # Game
        max_players_per_game = getattr(gs, "max_players", 4)
        grid_size = gs.grid_size
        game_timeout_seconds = 300  # Not present in new config, fallback
        # Logging
        debug = False

    return LegacySettings()
