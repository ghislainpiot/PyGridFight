"""Player-related Pydantic schemas for API."""

from datetime import datetime
from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field


class PlayerStatus(str, Enum):
    """Player status enumeration."""
    ONLINE = "online"
    OFFLINE = "offline"
    IN_GAME = "in_game"


class Position(BaseModel):
    """Position coordinates schema."""
    x: int = Field(..., ge=0, description="X coordinate")
    y: int = Field(..., ge=0, description="Y coordinate")


class PlayerStats(BaseModel):
    """Player statistics schema."""
    games_played: int = Field(default=0, ge=0, description="Total games played")
    games_won: int = Field(default=0, ge=0, description="Total games won")
    total_score: int = Field(default=0, ge=0, description="Total score across all games")
    average_score: float = Field(default=0.0, ge=0, description="Average score per game")


class PlayerProfile(BaseModel):
    """Player profile schema."""
    id: str = Field(..., description="Player ID")
    name: str = Field(..., min_length=1, max_length=50, description="Player name")
    status: PlayerStatus = Field(default=PlayerStatus.OFFLINE, description="Current status")
    created_at: datetime = Field(..., description="When player was created")
    last_seen: Optional[datetime] = Field(None, description="Last seen timestamp")
    stats: PlayerStats = Field(default_factory=PlayerStats, description="Player statistics")


class PlayerUpdateRequest(BaseModel):
    """Request schema for updating player profile."""
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="New player name")


class PlayerCreateRequest(BaseModel):
    """Request schema for creating a new player."""
    name: str = Field(..., min_length=1, max_length=50, description="Player name")


class PlayerResponse(BaseModel):
    """Response schema for player operations."""
    player: PlayerProfile = Field(..., description="Player profile")