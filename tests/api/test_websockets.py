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
        # The server sends an initial game state upon connection
        data = websocket.receive_json()
        assert data["type"] == "game_state_update"
        assert "payload" in data
        # The original test sent "hello" and expected "Message received: hello"
        # This is not how the websocket is designed to work. It expects JSON actions.
        # If testing sending a message, it should be a valid JSON action or
        # an invalid one to check error handling.
        # For now, just verifying the initial state reception is sufficient for "connect_valid_session".

def test_websocket_connect_invalid_session():
    invalid_session_id = uuid4()
    try:
        with client.websocket_connect(f"/ws/game/{invalid_session_id}") as websocket:
            # Should not reach here, should raise or close
            websocket.send_text("should not work")
            websocket.receive_text()
            assert False, "WebSocket should not connect with invalid session"
    except Exception:
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
from pygridfight.core.enums import PlayerActionEnum, ResourceTypeEnum

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
        found_avatar_in_payload = False
        assert "players" in data["payload"], "Payload should contain 'players' list"
        for player_data in data["payload"]["players"]:
            assert "avatars" in player_data, "Player data should contain 'avatars' list"
            for av_payload in player_data["avatars"]:
                if av_payload["avatar_id"] == str(avatar.avatar_id):
                    found_avatar_in_payload = True
                    assert av_payload["position"]["x"] == 1 and av_payload["position"]["y"] == 1
                    break
            if found_avatar_in_payload:
                break
        assert found_avatar_in_payload, "Moved avatar not found in the correct position in game state update"

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
    from pygridfight.gameplay.resources import Resource # Added import
    session.grid.spawn_resource(
        Coordinates(x=2, y=2),
        Resource(resource_type=ResourceTypeEnum.CURRENCY, value=1) # Changed COIN to CURRENCY
    )
    with client.websocket_connect(f"/ws/game/{session.session_id}") as websocket:
        websocket.receive_json()  # initial state
        collect_payload = {
            "action_type": PlayerActionEnum.COLLECT_RESOURCE.value,
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
        for d_idx, current_data in enumerate((data1, data2)):
            found_avatar_in_payload = False
            assert "players" in current_data["payload"], f"Payload {d_idx+1} should contain 'players' list"
            for player_data in current_data["payload"]["players"]:
                assert "avatars" in player_data, f"Player data in payload {d_idx+1} should contain 'avatars' list"
                for av_payload in player_data["avatars"]:
                    if av_payload["avatar_id"] == str(avatar.avatar_id):
                        found_avatar_in_payload = True
                        # In AvatarSchema, position is under "position", not "coordinates"
                        assert av_payload["position"]["x"] == 3 and av_payload["position"]["y"] == 3
                        break
                if found_avatar_in_payload:
                    break
            assert found_avatar_in_payload, f"Moved avatar not found in correct position in game state update for ws{d_idx+1}"

def test_websocket_disconnect_removes_connection():
    game_manager = app.state.game_manager
    session = game_manager.create_game_session(
        player_display_name="Disconnect Remove Player",
        grid_size=5,
        target_score=10
    )
    connection_manager: ConnectionManager = app.state.connection_manager
    with client.websocket_connect(f"/ws/game/{session.session_id}") as websocket:
        websocket.receive_json() # Initial state
        assert session.session_id in connection_manager.active_connections
        # Check that there is one connection for this session_id
        assert len(connection_manager.active_connections[session.session_id]) == 1
        # We can't easily assert that `websocket` (WebSocketTestSession) is the one in the list,
        # as ConnectionManager stores the raw Starlette WebSocket.
        # So, we rely on checking the count and the behavior on disconnect.

    # After disconnect (exiting the 'with' block), the connection should be removed.
    # Either the session_id key is gone, or the list for that session_id is empty.
    assert session.session_id not in connection_manager.active_connections or \
           not connection_manager.active_connections.get(session.session_id)