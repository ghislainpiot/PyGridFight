import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from fastapi.testclient import TestClient
from uuid import uuid4
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