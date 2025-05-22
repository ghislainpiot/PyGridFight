"""Configuration management for PyGridFight."""

import os
from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Server configuration
    host: str = Field(default="0.0.0.0", description="Host to bind the server to")
    port: int = Field(default=8000, description="Port to bind the server to")
    debug: bool = Field(default=False, description="Enable debug mode")

    # CORS configuration
    allowed_origins: List[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"],
        description="Allowed CORS origins"
    )

    # Game configuration
    max_players_per_game: int = Field(default=4, description="Maximum players per game")
    grid_size: int = Field(default=20, description="Default grid size")
    game_timeout_seconds: int = Field(default=300, description="Game timeout in seconds")

    # Logging configuration
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Log format (json or console)")

    class Config:
        """Pydantic configuration."""
        env_prefix = "PYGRIDFIGHT_"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()