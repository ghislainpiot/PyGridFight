"""Game-related Pydantic schemas for API."""

from datetime import datetime
from typing import List, Optional
from enum import Enum

from pydantic import BaseModel, Field


class GameStatus(str, Enum):
    """Game status enumeration."""
    WAITING = "waiting"
    ACTIVE = "active"
    FINISHED = "finished"
    CANCELLED = "cancelled"


class GameCreateRequest(BaseModel):
    """Request schema for creating a new game."""
    name: str = Field(..., min_length=1, max_length=100, description="Game name")
    max_players: int = Field(default=4, ge=2, le=8, description="Maximum number of players")
    grid_size: int = Field(default=20, ge=10, le=50, description="Grid size")
    is_private: bool = Field(default=False, description="Whether the game is private")


class GameJoinRequest(BaseModel):
    """Request schema for joining a game."""
    player_name: str = Field(..., min_length=1, max_length=50, description="Player name")


class PlayerInfo(BaseModel):
    """Player information schema."""
    id: str = Field(..., description="Player ID")
    name: str = Field(..., description="Player name")
    is_ready: bool = Field(default=False, description="Whether player is ready")
    joined_at: datetime = Field(..., description="When player joined")


class GameInfo(BaseModel):
    """Game information schema."""
    id: str = Field(..., description="Game ID")
    name: str = Field(..., description="Game name")
    status: GameStatus = Field(..., description="Current game status")
    max_players: int = Field(..., description="Maximum number of players")
    current_players: int = Field(..., description="Current number of players")
    grid_size: int = Field(..., description="Grid size")
    is_private: bool = Field(..., description="Whether the game is private")
    created_at: datetime = Field(..., description="When game was created")
    started_at: Optional[datetime] = Field(None, description="When game started")
    finished_at: Optional[datetime] = Field(None, description="When game finished")


class GameDetails(GameInfo):
    """Detailed game information schema."""
    players: List[PlayerInfo] = Field(default_factory=list, description="List of players")
    current_turn: Optional[str] = Field(None, description="Current player's turn")
    turn_number: int = Field(default=0, description="Current turn number")


class GameListResponse(BaseModel):
    """Response schema for listing games."""
    games: List[GameInfo] = Field(..., description="List of games")
    total: int = Field(..., description="Total number of games")


class GameCreateResponse(BaseModel):
    """Response schema for game creation."""
    game: GameDetails = Field(..., description="Created game details")
    player_id: str = Field(..., description="Creator's player ID")


class GameJoinResponse(BaseModel):
    """Response schema for joining a game."""
    game: GameDetails = Field(..., description="Game details")
    player_id: str = Field(..., description="Joined player's ID")