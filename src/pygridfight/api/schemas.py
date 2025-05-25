"""Pydantic schemas for API request/response validation and serialization."""

from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from ..core.enums import GameStatusEnum, ResourceTypeEnum, PlayerActionEnum

# --- Core Data Schemas ---

class CoordinatesSchema(BaseModel):
    """Schema for grid coordinates."""
    x: int
    y: int

    class Config:
        from_attributes = True

class ResourceSchema(BaseModel):
    """Schema for a resource on the grid."""
    resource_type: ResourceTypeEnum
    value: int

    class Config:
        from_attributes = True

class CellSchema(BaseModel):
    """Schema for a cell on the grid, which may contain a resource."""
    resource: Optional[ResourceSchema] = None

    class Config:
        from_attributes = True

# --- Avatar and Player Schemas ---

class AvatarSchema(BaseModel):
    """Schema for an avatar controlled by a player."""
    avatar_id: UUID
    player_id: UUID
    position: CoordinatesSchema
    # active_powerups: List[Any] # Defer for now

    class Config:
        from_attributes = True

class PlayerSchema(BaseModel):
    """Schema for a player in the game."""
    player_id: UUID
    display_name: str
    avatars: List[AvatarSchema]
    currency: int
    score: int

    class Config:
        from_attributes = True

# --- Game State Schemas ---

class GridSchema(BaseModel):
    """Schema for the game grid."""
    size: int
    cells: Dict[str, CellSchema]  # Key: "x,y" string for JSON compatibility

    class Config:
        from_attributes = True

class GameStateSchema(BaseModel):
    """Schema for the overall game state."""
    session_id: UUID
    status: GameStatusEnum
    current_turn: int
    grid: GridSchema
    players: List[PlayerSchema]
    target_score: int
    winner: Optional[UUID] = None

    class Config:
        from_attributes = True

# --- Request Schemas for Player Actions ---

class PlayerActionBaseSchema(BaseModel):
    """Base schema for player actions."""
    action_type: PlayerActionEnum
    avatar_id: UUID

class MoveActionPayloadSchema(BaseModel):
    """Payload for a move action."""
    target_coordinates: CoordinatesSchema

class MoveActionRequestSchema(PlayerActionBaseSchema):
    """Request schema for a move action."""
    # action_type is inherited from PlayerActionBaseSchema and validated by the calling code's if/elif
    # action_type: Literal[PlayerActionEnum.MOVE] = Field(
    #     default=PlayerActionEnum.MOVE, frozen=True
    # ) # This was causing the literal_error as 'data' contains string "MOVE"
    payload: MoveActionPayloadSchema

class CollectActionPayloadSchema(BaseModel):
    """Payload for a collect action."""
    target_coordinates: CoordinatesSchema

class CollectActionRequestSchema(PlayerActionBaseSchema):
    """Request schema for a collect action."""
    # action_type is inherited from PlayerActionBaseSchema and validated by the calling code's if/elif
    # action_type: Literal[PlayerActionEnum.COLLECT_RESOURCE] = Field(
    #     default=PlayerActionEnum.COLLECT_RESOURCE, frozen=True
    # ) # This was causing the literal_error
    payload: CollectActionPayloadSchema

# --- Request/Response Schemas for Game Lifecycle ---

class CreateGameRequestSchema(BaseModel):
    """Request schema for creating a new game session."""
    player_display_name: str
    grid_size: int = Field(default=10, ge=5, le=20)
    target_score: int = Field(default=100, ge=10)

# --- WebSocket Message Schemas ---

class WebSocketMessageSchema(BaseModel):
    """General schema for WebSocket messages."""
    type: str  # e.g., "game_update", "error", "player_action_confirmation"
    payload: Dict[str, Any]
