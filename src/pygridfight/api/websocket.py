"""WebSocket handlers for PyGridFight."""

from typing import Dict, Set
import json

from fastapi import WebSocket, WebSocketDisconnect
import structlog

from pygridfight.core.exceptions import GameError, PlayerError

logger = structlog.get_logger(__name__)


class ConnectionManager:
    """Manages WebSocket connections for the game."""

    def __init__(self) -> None:
        self.active_connections: Dict[str, WebSocket] = {}
        self.game_connections: Dict[str, Set[str]] = {}

    async def connect(self, websocket: WebSocket, player_id: str) -> None:
        """Accept a new WebSocket connection."""
        await websocket.accept()
        self.active_connections[player_id] = websocket
        logger.info("Player connected", player_id=player_id)

    def disconnect(self, player_id: str) -> None:
        """Remove a WebSocket connection."""
        if player_id in self.active_connections:
            del self.active_connections[player_id]

        # Remove from all games
        for game_id, players in self.game_connections.items():
            players.discard(player_id)

        logger.info("Player disconnected", player_id=player_id)

    def add_to_game(self, player_id: str, game_id: str) -> None:
        """Add a player to a game's connection group."""
        if game_id not in self.game_connections:
            self.game_connections[game_id] = set()
        self.game_connections[game_id].add(player_id)

    def remove_from_game(self, player_id: str, game_id: str) -> None:
        """Remove a player from a game's connection group."""
        if game_id in self.game_connections:
            self.game_connections[game_id].discard(player_id)

    async def send_personal_message(self, message: dict, player_id: str) -> None:
        """Send a message to a specific player."""
        if player_id in self.active_connections:
            websocket = self.active_connections[player_id]
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error("Failed to send message", player_id=player_id, error=str(e))
                self.disconnect(player_id)

    async def broadcast_to_game(self, message: dict, game_id: str) -> None:
        """Broadcast a message to all players in a game."""
        if game_id not in self.game_connections:
            return

        disconnected_players = []
        for player_id in self.game_connections[game_id]:
            if player_id in self.active_connections:
                try:
                    websocket = self.active_connections[player_id]
                    await websocket.send_text(json.dumps(message))
                except Exception as e:
                    logger.error("Failed to broadcast message", player_id=player_id, game_id=game_id, error=str(e))
                    disconnected_players.append(player_id)

        # Clean up disconnected players
        for player_id in disconnected_players:
            self.disconnect(player_id)


# Global connection manager instance
manager = ConnectionManager()


async def websocket_endpoint(websocket: WebSocket, player_id: str) -> None:
    """Main WebSocket endpoint for game communication."""
    await manager.connect(websocket, player_id)

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()

            try:
                message = json.loads(data)
                await handle_websocket_message(message, player_id)
            except json.JSONDecodeError:
                await manager.send_personal_message(
                    {"type": "error", "message": "Invalid JSON format"},
                    player_id
                )
            except (GameError, PlayerError) as e:
                await manager.send_personal_message(
                    {"type": "error", "message": e.message, "code": e.code},
                    player_id
                )
            except Exception as e:
                logger.error("Unexpected error handling message", player_id=player_id, error=str(e))
                await manager.send_personal_message(
                    {"type": "error", "message": "Internal server error"},
                    player_id
                )

    except WebSocketDisconnect:
        manager.disconnect(player_id)


async def handle_websocket_message(message: dict, player_id: str) -> None:
    """Handle incoming WebSocket messages."""
    message_type = message.get("type")

    if message_type == "ping":
        await manager.send_personal_message({"type": "pong"}, player_id)
    else:
        # TODO: Implement other message handlers
        logger.warning("Unknown message type", type=message_type, player_id=player_id)
        await manager.send_personal_message(
            {"type": "error", "message": f"Unknown message type: {message_type}"},
            player_id
        )