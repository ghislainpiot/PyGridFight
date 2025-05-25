import pytest
from uuid import UUID, uuid4
from typing import Any, Dict, List
from pydantic import ValidationError

from pygridfight.api.schemas import (
    CoordinatesSchema,
    ResourceSchema,
    CellSchema,
    AvatarSchema,
    PlayerSchema,
    GridSchema,
    GameStateSchema,
    PlayerActionBaseSchema,
    MoveActionPayloadSchema,
    MoveActionRequestSchema,
    CollectActionPayloadSchema,
    CollectActionRequestSchema,
    CreateGameRequestSchema,
    WebSocketMessageSchema,
)
from pygridfight.core.enums import GameStatusEnum, ResourceTypeEnum, PlayerActionEnum

# --- Mock domain objects for from_attributes tests ---

class MockCoordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class MockResource:
    def __init__(self, resource_type, value):
        self.resource_type = resource_type
        self.value = value

class MockCell:
    def __init__(self, resource=None):
        self.resource = resource

class MockAvatar:
    def __init__(self, avatar_id, player_id, position):
        self.avatar_id = avatar_id
        self.player_id = player_id
        self.position = position

class MockPlayer:
    def __init__(self, player_id, display_name, avatars, currency, score):
        self.player_id = player_id
        self.display_name = display_name
        self.avatars = avatars
        self.currency = currency
        self.score = score

class MockGrid:
    def __init__(self, size, cells):
        self.size = size
        self.cells = cells

class MockGameState:
    def __init__(self, session_id, status, current_turn, grid, players, target_score, winner=None):
        self.session_id = session_id
        self.status = status
        self.current_turn = current_turn
        self.grid = grid
        self.players = players
        self.target_score = target_score
        self.winner = winner

# --- CoordinatesSchema ---

def test_coordinates_schema_valid():
    data = {"x": 1, "y": 2}
    schema = CoordinatesSchema(**data)
    assert schema.x == 1
    assert schema.y == 2

def test_coordinates_schema_invalid():
    with pytest.raises(ValidationError):
        CoordinatesSchema(x="a", y=2)
    with pytest.raises(ValidationError):
        CoordinatesSchema(y=2)

def test_coordinates_schema_serialization():
    data = {"x": 3, "y": 4}
    schema = CoordinatesSchema(**data)
    out = schema.model_dump()
    assert out == data

def test_coordinates_schema_from_attributes():
    obj = MockCoordinates(5, 6)
    schema = CoordinatesSchema.model_validate(obj)
    assert schema.x == 5
    assert schema.y == 6

# --- ResourceSchema ---

def test_resource_schema_valid():
    data = {"resource_type": ResourceTypeEnum.GOLD, "value": 10}
    schema = ResourceSchema(**data)
    assert schema.resource_type == ResourceTypeEnum.GOLD
    assert schema.value == 10

def test_resource_schema_invalid():
    with pytest.raises(ValidationError):
        ResourceSchema(resource_type="not_a_type", value=10)
    with pytest.raises(ValidationError):
        ResourceSchema(value=10)

def test_resource_schema_serialization():
    data = {"resource_type": ResourceTypeEnum.GOLD, "value": 5}
    schema = ResourceSchema(**data)
    out = schema.model_dump()
    assert out == {"resource_type": ResourceTypeEnum.GOLD, "value": 5}

def test_resource_schema_from_attributes():
    obj = MockResource(ResourceTypeEnum.GOLD, 7)
    schema = ResourceSchema.model_validate(obj)
    assert schema.resource_type == ResourceTypeEnum.GOLD
    assert schema.value == 7

# --- CellSchema ---

def test_cell_schema_valid():
    resource = {"resource_type": ResourceTypeEnum.GOLD, "value": 1}
    data = {"resource": resource}
    schema = CellSchema(**data)
    assert schema.resource.resource_type == ResourceTypeEnum.GOLD

def test_cell_schema_none_resource():
    schema = CellSchema(resource=None)
    assert schema.resource is None

def test_cell_schema_invalid():
    with pytest.raises(ValidationError):
        CellSchema(resource={"resource_type": "not_a_type", "value": 1})

def test_cell_schema_serialization():
    resource = {"resource_type": ResourceTypeEnum.GOLD, "value": 2}
    schema = CellSchema(resource=resource)
    out = schema.model_dump()
    assert out["resource"]["resource_type"] == ResourceTypeEnum.GOLD

def test_cell_schema_from_attributes():
    obj = MockCell(MockResource(ResourceTypeEnum.GOLD, 3))
    schema = CellSchema.model_validate(obj)
    assert schema.resource.value == 3

# --- AvatarSchema ---

def test_avatar_schema_valid():
    aid = uuid4()
    pid = uuid4()
    pos = {"x": 1, "y": 2}
    data = {"avatar_id": aid, "player_id": pid, "position": pos}
    schema = AvatarSchema(**data)
    assert schema.avatar_id == aid
    assert schema.position.x == 1

def test_avatar_schema_invalid():
    with pytest.raises(ValidationError):
        AvatarSchema(avatar_id="not-a-uuid", player_id=uuid4(), position={"x": 1, "y": 2})

def test_avatar_schema_serialization():
    aid = uuid4()
    pid = uuid4()
    pos = {"x": 2, "y": 3}
    schema = AvatarSchema(avatar_id=aid, player_id=pid, position=pos)
    out = schema.model_dump()
    assert out["avatar_id"] == aid
    assert out["position"]["x"] == 2

def test_avatar_schema_from_attributes():
    aid = uuid4()
    pid = uuid4()
    obj = MockAvatar(aid, pid, MockCoordinates(7, 8))
    schema = AvatarSchema.model_validate(obj)
    assert schema.avatar_id == aid
    assert schema.position.x == 7

# --- PlayerSchema ---

def test_player_schema_valid():
    pid = uuid4()
    aid = uuid4()
    avatars = [{"avatar_id": aid, "player_id": pid, "position": {"x": 1, "y": 2}}]
    data = {
        "player_id": pid,
        "display_name": "Alice",
        "avatars": avatars,
        "currency": 100,
        "score": 10,
    }
    schema = PlayerSchema(**data)
    assert schema.display_name == "Alice"
    assert schema.avatars[0].avatar_id == aid

def test_player_schema_invalid():
    with pytest.raises(ValidationError):
        PlayerSchema(player_id=uuid4(), display_name="Bob", avatars=[], currency="not-int", score=0)

def test_player_schema_serialization():
    pid = uuid4()
    aid = uuid4()
    avatars = [{"avatar_id": aid, "player_id": pid, "position": {"x": 1, "y": 2}}]
    schema = PlayerSchema(
        player_id=pid, display_name="Alice", avatars=avatars, currency=50, score=5
    )
    out = schema.model_dump()
    assert out["display_name"] == "Alice"
    assert out["avatars"][0]["avatar_id"] == aid

def test_player_schema_from_attributes():
    pid = uuid4()
    aid = uuid4()
    avatar_obj = MockAvatar(aid, pid, MockCoordinates(1, 2))
    obj = MockPlayer(pid, "Eve", [avatar_obj], 200, 30)
    schema = PlayerSchema.model_validate(obj)
    assert schema.display_name == "Eve"
    assert schema.avatars[0].avatar_id == aid

# --- GridSchema ---

def test_grid_schema_valid():
    cell = {"resource": {"resource_type": ResourceTypeEnum.GOLD, "value": 1}}
    data = {"size": 10, "cells": {"1,2": cell}}
    schema = GridSchema(**data)
    assert schema.size == 10
    assert "1,2" in schema.cells
    assert schema.cells["1,2"].resource.value == 1

def test_grid_schema_invalid():
    with pytest.raises(ValidationError):
        GridSchema(size="not-int", cells={})

def test_grid_schema_serialization():
    cell = {"resource": {"resource_type": ResourceTypeEnum.GOLD, "value": 2}}
    schema = GridSchema(size=8, cells={"0,0": cell})
    out = schema.model_dump()
    assert out["size"] == 8
    assert "0,0" in out["cells"]

def test_grid_schema_from_attributes():
    cell_obj = MockCell(MockResource(ResourceTypeEnum.GOLD, 5))
    obj = MockGrid(12, {"3,4": cell_obj})
    schema = GridSchema.model_validate(obj)
    assert schema.size == 12
    assert "3,4" in schema.cells
    assert schema.cells["3,4"].resource.value == 5

# --- GameStateSchema ---

def test_game_state_schema_valid():
    sid = uuid4()
    pid = uuid4()
    aid = uuid4()
    player = {
        "player_id": pid,
        "display_name": "Alice",
        "avatars": [{"avatar_id": aid, "player_id": pid, "position": {"x": 1, "y": 2}}],
        "currency": 100,
        "score": 10,
    }
    grid = {"size": 10, "cells": {"1,2": {"resource": {"resource_type": ResourceTypeEnum.GOLD, "value": 1}}}}
    data = {
        "session_id": sid,
        "status": GameStatusEnum.IN_PROGRESS,
        "current_turn": 1,
        "grid": grid,
        "players": [player],
        "target_score": 100,
        "winner": None,
    }
    schema = GameStateSchema(**data)
    assert schema.session_id == sid
    assert schema.status == GameStatusEnum.IN_PROGRESS
    assert schema.players[0].display_name == "Alice"

def test_game_state_schema_invalid():
    with pytest.raises(ValidationError):
        GameStateSchema(
            session_id=uuid4(),
            status="not-a-status",
            current_turn=1,
            grid={"size": 10, "cells": {}},
            players=[],
            target_score=100,
        )

def test_game_state_schema_serialization():
    sid = uuid4()
    pid = uuid4()
    aid = uuid4()
    player = {
        "player_id": pid,
        "display_name": "Alice",
        "avatars": [{"avatar_id": aid, "player_id": pid, "position": {"x": 1, "y": 2}}],
        "currency": 100,
        "score": 10,
    }
    grid = {"size": 10, "cells": {"1,2": {"resource": {"resource_type": ResourceTypeEnum.GOLD, "value": 1}}}}
    schema = GameStateSchema(
        session_id=sid,
        status=GameStatusEnum.IN_PROGRESS,
        current_turn=1,
        grid=grid,
        players=[player],
        target_score=100,
        winner=None,
    )
    out = schema.model_dump()
    assert out["session_id"] == sid
    assert out["status"] == GameStatusEnum.IN_PROGRESS

def test_game_state_schema_from_attributes():
    sid = uuid4()
    pid = uuid4()
    aid = uuid4()
    avatar_obj = MockAvatar(aid, pid, MockCoordinates(1, 2))
    player_obj = MockPlayer(pid, "Alice", [avatar_obj], 100, 10)
    cell_obj = MockCell(MockResource(ResourceTypeEnum.GOLD, 1))
    grid_obj = MockGrid(10, {"1,2": cell_obj})
    obj = MockGameState(
        sid,
        GameStatusEnum.IN_PROGRESS,
        1,
        grid_obj,
        [player_obj],
        100,
        None,
    )
    schema = GameStateSchema.model_validate(obj)
    assert schema.session_id == sid
    assert schema.grid.size == 10
    assert schema.players[0].display_name == "Alice"

# --- PlayerActionBaseSchema ---

def test_player_action_base_schema_valid():
    aid = uuid4()
    data = {"action_type": PlayerActionEnum.MOVE, "avatar_id": aid}
    schema = PlayerActionBaseSchema(**data)
    assert schema.action_type == PlayerActionEnum.MOVE
    assert schema.avatar_id == aid

def test_player_action_base_schema_invalid():
    with pytest.raises(ValidationError):
        PlayerActionBaseSchema(action_type="not-an-action", avatar_id=uuid4())

# --- MoveActionPayloadSchema ---

def test_move_action_payload_schema_valid():
    data = {"target_coordinates": {"x": 1, "y": 2}}
    schema = MoveActionPayloadSchema(**data)
    assert schema.target_coordinates.x == 1

def test_move_action_payload_schema_invalid():
    with pytest.raises(ValidationError):
        MoveActionPayloadSchema(target_coordinates={"x": "a", "y": 2})

# --- MoveActionRequestSchema ---

def test_move_action_request_schema_valid():
    aid = uuid4()
    data = {
        "action_type": PlayerActionEnum.MOVE,
        "avatar_id": aid,
        "payload": {"target_coordinates": {"x": 1, "y": 2}},
    }
    schema = MoveActionRequestSchema(**data)
    assert schema.action_type == PlayerActionEnum.MOVE
    assert schema.payload.target_coordinates.x == 1

def test_move_action_request_schema_action_type_const():
    aid = uuid4()
    # Should fail if action_type is not MOVE
    with pytest.raises(ValidationError):
        MoveActionRequestSchema(
            action_type=PlayerActionEnum.COLLECT_RESOURCE,
            avatar_id=aid,
            payload={"target_coordinates": {"x": 1, "y": 2}},
        )

# --- CollectActionPayloadSchema ---

def test_collect_action_payload_schema_valid():
    data = {"target_coordinates": {"x": 1, "y": 2}}
    schema = CollectActionPayloadSchema(**data)
    assert schema.target_coordinates.x == 1

def test_collect_action_payload_schema_invalid():
    with pytest.raises(ValidationError):
        CollectActionPayloadSchema(target_coordinates={"x": "a", "y": 2})

# --- CollectActionRequestSchema ---

def test_collect_action_request_schema_valid():
    aid = uuid4()
    data = {
        "action_type": PlayerActionEnum.COLLECT_RESOURCE,
        "avatar_id": aid,
        "payload": {"target_coordinates": {"x": 1, "y": 2}},
    }
    schema = CollectActionRequestSchema(**data)
    assert schema.action_type == PlayerActionEnum.COLLECT_RESOURCE
    assert schema.payload.target_coordinates.x == 1

def test_collect_action_request_schema_action_type_const():
    aid = uuid4()
    # Should fail if action_type is not COLLECT
    with pytest.raises(ValidationError):
        CollectActionRequestSchema(
            action_type=PlayerActionEnum.MOVE,
            avatar_id=aid,
            payload={"target_coordinates": {"x": 1, "y": 2}},
        )

# --- CreateGameRequestSchema ---

def test_create_game_request_schema_valid():
    data = {"player_display_name": "Alice", "grid_size": 10, "target_score": 100}
    schema = CreateGameRequestSchema(**data)
    assert schema.player_display_name == "Alice"
    assert schema.grid_size == 10

def test_create_game_request_schema_defaults():
    data = {"player_display_name": "Bob"}
    schema = CreateGameRequestSchema(**data)
    assert schema.grid_size == 10
    assert schema.target_score == 100

def test_create_game_request_schema_invalid():
    with pytest.raises(ValidationError):
        CreateGameRequestSchema(player_display_name="Alice", grid_size=3, target_score=5)

# --- WebSocketMessageSchema ---

def test_websocket_message_schema_valid():
    data = {"type": "game_update", "payload": {"foo": "bar"}}
    schema = WebSocketMessageSchema(**data)
    assert schema.type == "game_update"
    assert schema.payload["foo"] == "bar"

def test_websocket_message_schema_invalid():
    with pytest.raises(ValidationError):
        WebSocketMessageSchema(type=123, payload={})

def test_websocket_message_schema_serialization():
    data = {"type": "error", "payload": {"error": "msg"}}
    schema = WebSocketMessageSchema(**data)
    out = schema.model_dump()
    assert out["type"] == "error"
    assert out["payload"]["error"] == "msg"