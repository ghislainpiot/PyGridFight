"""Action-related Pydantic schemas for API."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from pygridfight.api.schemas.player import Position


class ActionType(str, Enum):
    """Action type enumeration."""

    MOVE = "move"
    ATTACK = "attack"
    COLLECT = "collect"
    USE_ITEM = "use_item"
    END_TURN = "end_turn"


class ActionStatus(str, Enum):
    """Action status enumeration."""

    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    INVALID = "invalid"


class BaseAction(BaseModel):
    """Base action schema."""

    type: ActionType = Field(..., description="Type of action")
    player_id: str = Field(..., description="Player performing the action")


class MoveAction(BaseAction):
    """Move action schema."""

    type: ActionType = Field(default=ActionType.MOVE, description="Action type")
    target_position: Position = Field(..., description="Target position to move to")


class AttackAction(BaseAction):
    """Attack action schema."""

    type: ActionType = Field(default=ActionType.ATTACK, description="Action type")
    target_position: Position = Field(..., description="Position to attack")
    weapon_id: str | None = Field(None, description="Weapon to use for attack")


class CollectAction(BaseAction):
    """Collect resource action schema."""

    type: ActionType = Field(default=ActionType.COLLECT, description="Action type")
    target_position: Position = Field(
        ..., description="Position of resource to collect"
    )


class UseItemAction(BaseAction):
    """Use item action schema."""

    type: ActionType = Field(default=ActionType.USE_ITEM, description="Action type")
    item_id: str = Field(..., description="ID of item to use")
    target_position: Position | None = Field(
        None, description="Target position for item use"
    )


class EndTurnAction(BaseAction):
    """End turn action schema."""

    type: ActionType = Field(default=ActionType.END_TURN, description="Action type")


class ActionRequest(BaseModel):
    """Generic action request schema."""

    action: dict[str, Any] = Field(..., description="Action data")


class ActionResult(BaseModel):
    """Action result schema."""

    action_id: str = Field(..., description="Unique action ID")
    status: ActionStatus = Field(..., description="Action status")
    message: str | None = Field(None, description="Result message")
    data: dict[str, Any] | None = Field(None, description="Additional result data")


class ActionResponse(BaseModel):
    """Response schema for action execution."""

    result: ActionResult = Field(..., description="Action execution result")
