from typing import Dict, List
from uuid import UUID
from fastapi import WebSocket

class ConnectionManager:
    """
    Manages active WebSocket connections for each game session.
    """
    def __init__(self) -> None:
        self.active_connections: Dict[UUID, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, session_id: UUID) -> None:
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
        self.active_connections[session_id].append(websocket)

    def disconnect(self, websocket: WebSocket, session_id: UUID) -> None:
        if session_id in self.active_connections:
            try:
                self.active_connections[session_id].remove(websocket)
            except ValueError:
                pass
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]

    async def broadcast(self, message: str, session_id: UUID) -> None:
        if session_id in self.active_connections:
            for connection in self.active_connections[session_id]:
                await connection.send_text(message)

    async def broadcast_json(self, data: dict, session_id: UUID) -> None:
        if session_id in self.active_connections:
            for connection in self.active_connections[session_id]:
                await connection.send_json(data)