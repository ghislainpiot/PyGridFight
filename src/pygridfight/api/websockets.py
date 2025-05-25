from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from uuid import UUID
from pygridfight.game_lifecycle.exceptions import GameNotFoundError

ws_router = APIRouter()

@ws_router.websocket("/ws/game/{session_id}")
async def websocket_game_endpoint(websocket: WebSocket, session_id: UUID):
    """
    WebSocket endpoint for real-time game communication.

    Args:
        websocket (WebSocket): The WebSocket connection.
        session_id (UUID): The game session ID.

    Behavior:
        - Accepts connection if session exists, else closes with error.
        - Echoes received messages for MVP.
        - Logs connect/disconnect events.
    """
    game_manager = websocket.app.state.game_manager
    try:
        game_session = game_manager.get_game_session_or_raise(session_id)
    except GameNotFoundError:
        await websocket.close(code=4004)
        return
    await websocket.accept()
    print(f"Player connected to game {session_id}")
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Game {session_id}: Received message: {data}")
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        print(f"Player disconnected from game {session_id}")
    except Exception as e:
        print(f"Error in WebSocket for game {session_id}: {e}")
        await websocket.close(code=1011)
    finally:
        print(f"Cleaning up WebSocket for game {session_id}")