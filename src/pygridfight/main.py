from fastapi import APIRouter, FastAPI

from pygridfight.api.connection_manager import ConnectionManager
from pygridfight.api.converters import convert_game_session_to_schema
from pygridfight.api.schemas import (
    CreateGameRequestSchema,
    GameStateSchema,
)
from pygridfight.api.websockets import ws_router
from pygridfight.game_lifecycle.manager import GameLifecycleManager
from pygridfight.gameplay.session import GameSession

app = FastAPI(title="PyGridFight API")
game_manager = GameLifecycleManager()
connection_manager = ConnectionManager()
app.state.connection_manager = connection_manager
api_router = APIRouter()


@api_router.post("/game", response_model=GameStateSchema, status_code=201)
async def create_game(request: CreateGameRequestSchema) -> GameStateSchema:
    """
    Create a new game session and start the game.

    Args:
        request (CreateGameRequestSchema): The request body containing player display name, grid size, and target score.

    Returns:
        GameStateSchema: The initial state of the created game.
    """
    session = game_manager.create_game_session(
        player_display_name=request.player_display_name,
        grid_size=request.grid_size,
        target_score=request.target_score
    )
    session.start_game()
    return convert_game_session_to_schema(session)

# Set game_manager in app state for use in WebSocket endpoints
app.state.game_manager = game_manager

# Import and include WebSocket router

app.include_router(api_router, prefix="/api/v1")
app.include_router(ws_router)
