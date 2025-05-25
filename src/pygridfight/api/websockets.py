from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from uuid import UUID
from pydantic import ValidationError
from pygridfight.core.models import Coordinates # Add import
from pygridfight.game_lifecycle.exceptions import GameNotFoundError
from pygridfight.api.connection_manager import ConnectionManager
from pygridfight.api.schemas import (
    MoveActionRequestSchema,
    CollectActionRequestSchema,
    WebSocketMessageSchema,
)
from pygridfight.gameplay.actions import MoveAction, CollectAction
from pygridfight.core.enums import PlayerActionEnum
from pygridfight.main import convert_game_session_to_schema

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
        - Handles player actions, broadcasts state, and manages connections.
    """
    game_manager = websocket.app.state.game_manager
    connection_manager: ConnectionManager = websocket.app.state.connection_manager
    try:
        game_session = game_manager.get_game_session_or_raise(session_id)
    except GameNotFoundError:
        await websocket.close(code=4004)
        return

    await connection_manager.connect(websocket, session_id)
    print(f"Player connected to game {session_id}")

    # Send initial game state
    try:
        from fastapi.encoders import jsonable_encoder
        initial_state_schema = convert_game_session_to_schema(game_session)
        initial_message = WebSocketMessageSchema(
            type="game_state_update",
            payload=initial_state_schema.model_dump()
        )
        await websocket.send_json(jsonable_encoder(initial_message.model_dump()))

        while True:
            data = await websocket.receive_json()
            print(f"Received WebSocket data: {data}") # Add log
            try:
                message_type = data.get("action_type")
                payload = data.get("payload")
                avatar_id_str = data.get("avatar_id")
                if not message_type or not payload or not avatar_id_str:
                    raise ValueError("Missing action_type, payload, or avatar_id")
                avatar_id = UUID(avatar_id_str)

                domain_action = None
                if message_type == PlayerActionEnum.MOVE.value:
                    action_schema = MoveActionRequestSchema(**data)
                    domain_action = MoveAction(
                        avatar_id=action_schema.avatar_id,
                        target_coordinates=Coordinates(
                            x=action_schema.payload.target_coordinates.x,
                            y=action_schema.payload.target_coordinates.y
                        )
                    )
                elif message_type == PlayerActionEnum.COLLECT_RESOURCE.value:
                    action_schema = CollectActionRequestSchema(**data)
                    domain_action = CollectAction(
                        avatar_id=action_schema.avatar_id,
                        target_coordinates=Coordinates(
                            x=action_schema.payload.target_coordinates.x,
                            y=action_schema.payload.target_coordinates.y
                        )
                    )
                else:
                    error_msg = WebSocketMessageSchema(
                        type="error",
                        payload={"message": f"Unknown action type: {message_type}"}
                    )
                    from fastapi.encoders import jsonable_encoder
                    await websocket.send_json(jsonable_encoder(error_msg.model_dump()))
                    continue

                if domain_action:
                    game_session.process_player_action(domain_action)
                    updated_state_schema = convert_game_session_to_schema(game_session)
                    broadcast_message = WebSocketMessageSchema(
                        type="game_state_update",
                        payload=updated_state_schema.model_dump()
                    )
                    from fastapi.encoders import jsonable_encoder
                    await connection_manager.broadcast_json(
                        jsonable_encoder(broadcast_message.model_dump()), session_id
                    )

            except ValidationError as e:
                print(f"ValidationError in WebSocket: {e.errors()}") # Add log
                error_msg = WebSocketMessageSchema(
                    type="error",
                    payload={"message": "Invalid action format", "details": e.errors()}
                )
                from fastapi.encoders import jsonable_encoder
                await websocket.send_json(jsonable_encoder(error_msg.model_dump()))
            except ValueError as e:
                print(f"ValueError in WebSocket: {str(e)}") # Add log
                error_msg = WebSocketMessageSchema(
                    type="error",
                    payload={"message": str(e)}
                )
                from fastapi.encoders import jsonable_encoder
                await websocket.send_json(jsonable_encoder(error_msg.model_dump()))
            except Exception as e:
                print(f"Error processing action in game {session_id}: {e}")
                error_msg = WebSocketMessageSchema(
                    type="error",
                    payload={"message": f"Error processing action: {str(e)}"}
                )
                await websocket.send_json(error_msg.model_dump())

    except WebSocketDisconnect:
        print(f"Player disconnected from game {session_id}")
    except Exception as e:
        print(f"Error in WebSocket for game {session_id}: {e}")
        await websocket.close(code=1011)
    finally:
        connection_manager.disconnect(websocket, session_id)
        print(f"Cleaning up WebSocket for game {session_id}")