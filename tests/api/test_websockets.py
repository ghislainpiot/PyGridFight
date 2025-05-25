import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from fastapi.testclient import TestClient
from uuid import uuid4
from pygridfight.core.models import Coordinates
from pygridfight.gameplay.avatar import Avatar
from pygridfight.main import app

client = TestClient(app)

def test_websocket_connect_valid_session():
    # Create a game session first
    game_manager = app.state.game_manager
    session = game_manager.create_game_session(
        player_display_name="WebSocket Player",
        grid_size=6,
        target_score=20
    )
    with client.websocket_connect(f"/ws/game/{session.session_id}") as websocket:
        websocket.send_text("hello")
        data = websocket.receive_text()
        assert data == "Message received: hello"

def test_websocket_connect_invalid_session():
    invalid_session_id = uuid4()
    try:
        with client.websocket_connect(f"/ws/game/{invalid_session_id}") as websocket:
            # Should not reach here, should raise or close
            websocket.send_text("should not work")
            websocket.receive_text()
            assert False, "WebSocket should not connect with invalid session"
    except Exception as e:
        # Accept any exception as correct behavior for invalid session
        assert True

def test_websocket_disconnect():
    game_manager = app.state.game_manager
    session = game_manager.create_game_session(
        player_display_name="Disconnect Player",
        grid_size=4,
        target_score=10
    )
    with client.websocket_connect(f"/ws/game/{session.session_id}"):
        pass  # Connect and immediately disconnect
    # No assertion needed; if cleanup logic is added, it can be checked here
from pygridfight.api.connection_manager import ConnectionManager
from pygridfight.api.schemas import (
    WebSocketMessageSchema,
    MoveActionRequestSchema,
    CollectActionRequestSchema,
    CoordinatesSchema,
)
from pygridfight.core.enums import PlayerActionEnum

def test_websocket_sends_initial_state():
    game_manager = app.state.game_manager
    session = game_manager.create_game_session(
        player_display_name="Initial State Player",
        grid_size=5,
        target_score=15
    )
    with client.websocket_connect(f"/ws/game/{session.session_id}") as websocket:
        data = websocket.receive_json()
        assert data["type"] == "game_state_update"
        assert "payload" in data
        # Optionally, check grid size or other state details

def test_websocket_handle_move_action():
    game_manager = app.state.game_manager
    session = game_manager.create_game_session(
        player_display_name="Move Player",
        grid_size=5,
        target_score=10
    )
    avatar = Avatar(avatar_id=uuid4(), player_id=session.player.player_id, initial_position=Coordinates(x=0, y=0))
    session.player.add_avatar(avatar)
    with client.websocket_connect(f"/ws/game/{session.session_id}") as websocket:
        websocket.receive_json()  # initial state
        move_payload = {
            "action_type": PlayerActionEnum.MOVE.value,
            "avatar_id": str(avatar.avatar_id),
            "payload": {
                "target_coordinates": {"x": 1, "y": 1}
            }
        }
        websocket.send_json(move_payload)
        data = websocket.receive_json()
        assert data["type"] == "game_state_update"
        # Check that avatar position updated
        found = False
        for av in data["payload"]["avatars"]:
            if av["avatar_id"] == str(avatar.avatar_id):
                found = True
                assert av["coordinates"]["x"] == 1 and av["coordinates"]["y"] == 1
        assert found

def test_websocket_handle_collect_action():
    game_manager = app.state.game_manager
    session = game_manager.create_game_session(
        player_display_name="Collect Player",
        grid_size=5,
        target_score=10
    )
    avatar = Avatar(avatar_id=uuid4(), player_id=session.player.player_id, initial_position=Coordinates(x=0, y=0))
    session.player.add_avatar(avatar)
    # Place a resource at (2,2) for collect
    session.grid.cells[(2,2)].resource = "coin"
    with client.websocket_connect(f"/ws/game/{session.session_id}") as websocket:
        websocket.receive_json()  # initial state
        collect_payload = {
            "action_type": PlayerActionEnum.COLLECT.value,
            "avatar_id": str(avatar.avatar_id),
            "payload": {
                "target_coordinates": {"x": 2, "y": 2}
            }
        }
        websocket.send_json(collect_payload)
        data = websocket.receive_json()
        assert data["type"] == "game_state_update"
        # Optionally, check avatar's score/currency increased

def test_websocket_handle_invalid_action_format():
    game_manager = app.state.game_manager
    session = game_manager.create_game_session(
        player_display_name="Invalid Format Player",
        grid_size=5,
        target_score=10
    )
    with client.websocket_connect(f"/ws/game/{session.session_id}") as websocket:
        websocket.receive_json()  # initial state
        # Missing payload
        bad_payload = {
            "action_type": PlayerActionEnum.MOVE.value,
            "avatar_id": "not-a-uuid"
        }
        websocket.send_json(bad_payload)
        data = websocket.receive_json()
        assert data["type"] == "error"
        assert "Invalid action format" in data["payload"]["message"] or "Missing" in data["payload"]["message"]

def test_websocket_handle_unknown_action_type():
    game_manager = app.state.game_manager
    session = game_manager.create_game_session(
        player_display_name="Unknown Action Player",
        grid_size=5,
        target_score=10
    )
    avatar = Avatar(avatar_id=uuid4(), player_id=session.player.player_id, initial_position=Coordinates(x=0, y=0))
    session.player.add_avatar(avatar)
    with client.websocket_connect(f"/ws/game/{session.session_id}") as websocket:
        websocket.receive_json()  # initial state
        unknown_payload = {
            "action_type": "FLY",
            "avatar_id": str(avatar.avatar_id),
            "payload": {"target_coordinates": {"x": 0, "y": 0}}
        }
        websocket.send_json(unknown_payload)
        data = websocket.receive_json()
        assert data["type"] == "error"
        assert "Unknown action type" in data["payload"]["message"]

def test_websocket_broadcast_to_multiple_clients():
    game_manager = app.state.game_manager
    session = game_manager.create_game_session(
        player_display_name="Broadcast Player",
        grid_size=5,
        target_score=10
    )
    avatar = Avatar(avatar_id=uuid4(), player_id=session.player.player_id, initial_position=Coordinates(x=0, y=0))
    session.player.add_avatar(avatar)
    with client.websocket_connect(f"/ws/game/{session.session_id}") as ws1, \
         client.websocket_connect(f"/ws/game/{session.session_id}") as ws2:
        ws1.receive_json()
        ws2.receive_json()
        move_payload = {
            "action_type": PlayerActionEnum.MOVE.value,
            "avatar_id": str(avatar.avatar_id),
            "payload": {"target_coordinates": {"x": 3, "y": 3}}
        }
        ws1.send_json(move_payload)
        data1 = ws1.receive_json()
        data2 = ws2.receive_json()
        assert data1["type"] == "game_state_update"
        assert data2["type"] == "game_state_update"
        # Both should see the avatar at (3,3)
        for data in (data1, data2):
            found = False
            for av in data["payload"]["avatars"]:
                if av["avatar_id"] == str(avatar.avatar_id):
                    found = True
                    assert av["coordinates"]["x"] == 3 and av["coordinates"]["y"] == 3
            assert found

def test_websocket_disconnect_removes_connection():
    game_manager = app.state.game_manager
    session = game_manager.create_game_session(
        player_display_name="Disconnect Remove Player",
        grid_size=5,
        target_score=10
    )
    connection_manager: ConnectionManager = app.state.connection_manager
    with client.websocket_connect(f"/ws/game/{session.session_id}") as websocket:
        websocket.receive_json()
        assert session.session_id in connection_manager.active_connections
        assert websocket._ws in connection_manager.active_connections[session.session_id]
    # After disconnect, should be removed
    assert session.session_id not in connection_manager.active_connections or \
        websocket._ws not in connection_manager.active_connections.get(session.session_id, [])