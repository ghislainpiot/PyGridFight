"""WebSocket message schemas for API."""

from typing import Optional, Dict, Any, Union
from enum import Enum

from pydantic import BaseModel, Field

from pygridfight.api.schemas.actions import ActionResult
from pygridfight.api.schemas.game import GameDetails
from pygridfight.api.schemas.player import PlayerProfile


class MessageType(str, Enum):
    """WebSocket message type enumeration."""
    # Client to server
    PING = "ping"
    JOIN_GAME = "join_game"
    LEAVE_GAME = "leave_game"
    PLAYER_ACTION = "player_action"
    PLAYER_READY = "player_ready"

    # Server to client
    PONG = "pong"
    ERROR = "error"
    GAME_STATE = "game_state"
    PLAYER_JOINED = "player_joined"
    PLAYER_LEFT = "player_left"
    GAME_STARTED = "game_started"
    GAME_ENDED = "game_ended"
    TURN_CHANGED = "turn_changed"
    ACTION_RESULT = "action_result"


class BaseMessage(BaseModel):
    """Base WebSocket message schema."""
    type: MessageType = Field(..., description="Message type")
    timestamp: Optional[str] = Field(None, description="Message timestamp")


class PingMessage(BaseMessage):
    """Ping message schema."""
    type: MessageType = Field(default=MessageType.PING, description="Message type")


class PongMessage(BaseMessage):
    """Pong message schema."""
    type: MessageType = Field(default=MessageType.PONG, description="Message type")


class ErrorMessage(BaseMessage):
    """Error message schema."""
    type: MessageType = Field(default=MessageType.ERROR, description="Message type")
    message: str = Field(..., description="Error message")
    code: Optional[str] = Field(None, description="Error code")


class JoinGameMessage(BaseMessage):
    """Join game message schema."""
    type: MessageType = Field(default=MessageType.JOIN_GAME, description="Message type")
    game_id: str = Field(..., description="Game ID to join")
    player_name: str = Field(..., description="Player name")


class LeaveGameMessage(BaseMessage):
    """Leave game message schema."""
    type: MessageType = Field(default=MessageType.LEAVE_GAME, description="Message type")
    game_id: str = Field(..., description="Game ID to leave")


class PlayerActionMessage(BaseMessage):
    """Player action message schema."""
    type: MessageType = Field(default=MessageType.PLAYER_ACTION, description="Message type")
    action: Dict[str, Any] = Field(..., description="Action data")


class PlayerReadyMessage(BaseMessage):
    """Player ready message schema."""
    type: MessageType = Field(default=MessageType.PLAYER_READY, description="Message type")
    ready: bool = Field(..., description="Ready status")


class GameStateMessage(BaseMessage):
    """Game state message schema."""
    type: MessageType = Field(default=MessageType.GAME_STATE, description="Message type")
    game: GameDetails = Field(..., description="Current game state")


class PlayerJoinedMessage(BaseMessage):
    """Player joined message schema."""
    type: MessageType = Field(default=MessageType.PLAYER_JOINED, description="Message type")
    player: PlayerProfile = Field(..., description="Player who joined")
    game_id: str = Field(..., description="Game ID")


class PlayerLeftMessage(BaseMessage):
    """Player left message schema."""
    type: MessageType = Field(default=MessageType.PLAYER_LEFT, description="Message type")
    player_id: str = Field(..., description="Player ID who left")
    game_id: str = Field(..., description="Game ID")


class GameStartedMessage(BaseMessage):
    """Game started message schema."""
    type: MessageType = Field(default=MessageType.GAME_STARTED, description="Message type")
    game: GameDetails = Field(..., description="Started game details")


class GameEndedMessage(BaseMessage):
    """Game ended message schema."""
    type: MessageType = Field(default=MessageType.GAME_ENDED, description="Message type")
    game_id: str = Field(..., description="Game ID")
    winner_id: Optional[str] = Field(None, description="Winner player ID")
    reason: str = Field(..., description="Reason for game end")


class TurnChangedMessage(BaseMessage):
    """Turn changed message schema."""
    type: MessageType = Field(default=MessageType.TURN_CHANGED, description="Message type")
    current_player_id: str = Field(..., description="Current player's turn")
    turn_number: int = Field(..., description="Turn number")


class ActionResultMessage(BaseMessage):
    """Action result message schema."""
    type: MessageType = Field(default=MessageType.ACTION_RESULT, description="Message type")
    result: ActionResult = Field(..., description="Action execution result")


# Union type for all possible messages
WebSocketMessage = Union[
    PingMessage,
    PongMessage,
    ErrorMessage,
    JoinGameMessage,
    LeaveGameMessage,
    PlayerActionMessage,
    PlayerReadyMessage,
    GameStateMessage,
    PlayerJoinedMessage,
    PlayerLeftMessage,
    GameStartedMessage,
    GameEndedMessage,
    TurnChangedMessage,
    ActionResultMessage,
]