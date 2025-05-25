from fastapi import FastAPI, APIRouter
from pygridfight.game_lifecycle.manager import GameLifecycleManager
from pygridfight.api.schemas import (
    CreateGameRequestSchema,
    GameStateSchema,
    PlayerSchema,
    AvatarSchema,
    GridSchema,
    CellSchema,
)
from pygridfight.gameplay.session import GameSession

from pygridfight.api.connection_manager import ConnectionManager

app = FastAPI(title="PyGridFight API")
game_manager = GameLifecycleManager()
connection_manager = ConnectionManager()
app.state.connection_manager = connection_manager
api_router = APIRouter()

def convert_game_session_to_schema(session: GameSession) -> GameStateSchema:
    """
    Convert a GameSession domain object to a GameStateSchema for API responses.

    Args:
        session (GameSession): The game session to convert.

    Returns:
        GameStateSchema: The API schema representation of the game state.
    """
    # Convert grid cells: Dict[Coordinates, Cell] -> Dict[str, CellSchema]
    grid_schema_cells = {
        f"{coords.x},{coords.y}": CellSchema.model_validate(cell)
        for coords, cell in session.grid.cells.items()
    }
    grid_schema = GridSchema(
        size=session.grid.size,
        cells=grid_schema_cells
    )
    # Convert avatars
    avatar_schemas = [
        AvatarSchema.model_validate(avatar)
        for avatar in session.player.avatars
    ]
    # Player score
    player_score = session.score_keeper.get_score(session.player.player_id)
    player_schema = PlayerSchema(
        player_id=session.player.player_id,
        display_name=session.player.display_name,
        avatars=avatar_schemas,
        currency=session.player.currency,
        score=player_score if player_score is not None else 0
    )
    return GameStateSchema(
        session_id=session.session_id,
        status=session.status,
        current_turn=session.current_turn,
        grid=grid_schema,
        players=[player_schema],
        target_score=session.target_score,
        winner=session.winner
    )

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
from pygridfight.api.websockets import ws_router
app.include_router(api_router, prefix="/api/v1")
app.include_router(ws_router)
