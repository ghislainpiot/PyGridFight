"""REST API endpoints for PyGridFight."""

from fastapi import APIRouter, HTTPException, status, Depends, Request
import structlog
from fastapi.responses import JSONResponse

from pygridfight.core.exceptions import (
    GameNotFoundError,
    GameFullError,
    PlayerNotFoundError,
    InvalidActionError,
    ValidationError,
    GameError,
    PlayerError,
)
from pygridfight.api.schemas.game import (
    GameCreateRequest,
    GameCreateResponse,
    GameJoinRequest,
    GameJoinResponse,
    GameListResponse,
    GameDetails,
    GameLeaveRequest,
    GameLeaveResponse,
)
from pygridfight.domain.models.game import GameSettings
from pygridfight.infrastructure.game_state import GameStateManager

logger = structlog.get_logger(__name__)

def get_game_state_manager() -> GameStateManager:
    # Singleton pattern or however GameStateManager is meant to be instantiated
    return GameStateManager()

router = APIRouter()


@router.route("/health", methods=["GET", "OPTIONS"])
async def health_check(request) -> JSONResponse:
    """Health check endpoint with system/config info and timestamp."""
    import platform
    import time
    from pygridfight.core.config import get_settings

    settings = get_settings()
    return JSONResponse(content={
        "status": "healthy",
        "service": "pygridfight",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "system": {
            "python_version": platform.python_version(),
            "platform": platform.system(),
            "release": platform.release(),
        },
        "config": {
            "host": settings.host,
            "port": settings.port,
            "grid_size": getattr(settings, "grid_size", None),
            "max_players": getattr(settings, "max_players", None),
        },
    })


@router.get("/games")
async def list_games(
    manager: GameStateManager = Depends(get_game_state_manager)
):
    """List all active games."""
    try:
        game_ids = await manager.list_active_games()
        games = []
        for gid in game_ids:
            game = await manager.get_game(gid)
            if game:
                state = game.get_state()
                state.update({
                    "max_players": None,
                    "grid_size": None,
                    "is_private": None,
                    "created_at": None,
                    "started_at": None,
                    "finished_at": None,
                    "current_players": len(game.players),
                    "players": list(game.players.keys()),
                    "current_turn": None,
                    "turn_number": game.turn,
                })
                games.append(state)
        return {"games": games, "total": len(games)}
    except Exception as e:
        logger.error("Failed to list games", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/games", status_code=201)
async def create_game(
    req: GameCreateRequest,
    manager: GameStateManager = Depends(get_game_state_manager)
):
    """Create a new game."""
    import uuid

    game_id = str(uuid.uuid4())
    try:
        # For now, pass only the required fields to Game
        # Create GameSettings from request
        settings = GameSettings(
            name=req.name,
            max_players=req.max_players,
            grid_size=req.grid_size,
            is_private=req.is_private,
        )
        game = await manager.create_game(game_id, settings)
        # Persist metadata (redundant, but ensures all fields are set)
        game.name = req.name
        game.max_players = req.max_players
        game.grid_size = req.grid_size
        game.is_private = req.is_private
        await manager.update_game(game_id, game)
        # Assume the creator is also the first player (not implemented)
        player_id = str(uuid.uuid4())
        game = await manager.get_game(game_id)
        state = game.get_state()
        state.update({
            "name": req.name,
            "max_players": req.max_players,
            "grid_size": req.grid_size,
            "is_private": req.is_private,
            "created_at": getattr(game, "created_at", None),
            "started_at": getattr(game, "started_at", None),
            "finished_at": getattr(game, "finished_at", None),
            "current_players": len(game.players),
            "players": list(game.players.keys()),
            "current_turn": None,
            "turn_number": game.turn,
        })
        return {
            "game": state,
            "player_id": player_id
        }
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.message)
    except Exception as e:
        logger.error("Failed to create game", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/games/{game_id}")
async def get_game(
    game_id: str,
    manager: GameStateManager = Depends(get_game_state_manager)
):
    """Get game details."""
    try:
        game = await manager.get_game(game_id)
        if not game:
            raise GameNotFoundError(f"Game {game_id} not found")
        state = game.get_state()
        state.update({
            "name": getattr(game, "name", None),
            "max_players": getattr(game, "max_players", None),
            "grid_size": getattr(game, "grid_size", None),
            "is_private": getattr(game, "is_private", None),
            "created_at": getattr(game, "created_at", None),
            "started_at": getattr(game, "started_at", None),
            "finished_at": getattr(game, "finished_at", None),
            "current_players": len(game.players),
            "players": list(game.players.keys()),
            "current_turn": None,
            "turn_number": game.turn,
        })
        return state
    except GameNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": str(e)}
        )
    except Exception as e:
        logger.error("Failed to get game", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/games/{game_id}/join")
async def join_game(
    game_id: str,
    req: GameJoinRequest,
    manager: GameStateManager = Depends(get_game_state_manager)
):
    """Join an existing game."""
    import uuid
    from pygridfight.domain.models.player import Player
    try:
        game = await manager.get_game(game_id)
        if not game:
            raise GameNotFoundError(f"Game {game_id} not found")
        max_players = getattr(game, "max_players", 4)
        if len(game.players) >= max_players:
            raise GameFullError(f"Game {game_id} is full")
        # Generate a new player and add to the game
        player_id = str(uuid.uuid4())
        player = Player(id=player_id, display_name=req.player_name)
        try:
            game.add_player(player)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        # Persist the updated game state
        await manager.update_game(game_id, game)
        game = await manager.get_game(game_id)
        state = game.get_state()
        state.update({
            "name": getattr(game, "name", None),
            "max_players": max_players,
            "grid_size": getattr(game, "grid_size", None),
            "is_private": getattr(game, "is_private", None),
            "created_at": getattr(game, "created_at", None),
            "started_at": getattr(game, "started_at", None),
            "finished_at": getattr(game, "finished_at", None),
            "current_players": len(game.players),
            "players": list(game.players.keys()),
            "current_turn": None,
            "turn_number": game.turn,
        })
        return {
            "game": state,
            "player_id": player_id
        }
    except GameNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": str(e)}
        )
    except GameFullError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e)}
        )
    except Exception as e:
        logger.error("Failed to join game", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/games/{game_id}", status_code=204)
async def delete_game(
    game_id: str,
    manager: GameStateManager = Depends(get_game_state_manager)
):
    """End a game (delete)."""
    try:
        game = await manager.get_game(game_id)
        if not game:
            raise GameNotFoundError(f"Game {game_id} not found")
        await manager.delete_game(game_id)
        return JSONResponse(status_code=204, content=None)
    except GameNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": str(e)}
        )
    except Exception as e:
        logger.error("Failed to delete game", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/games/{game_id}/leave", response_model=GameLeaveResponse)
async def leave_game(
    game_id: str,
    req: GameLeaveRequest,
    manager: GameStateManager = Depends(get_game_state_manager)
) -> GameLeaveResponse:
    """Leave a game."""
    try:
        game = await manager.get_game(game_id)
        if not game:
            raise GameNotFoundError(f"Game {game_id} not found")
        # await manager.remove_player(game_id, req.player_id)
        return GameLeaveResponse(
            message=f"Player {req.player_id} left game {game_id}",
            player_id=req.player_id
        )
    except GameNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": str(e)}
        )
    except PlayerNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": str(e)}
        )
    except Exception as e:
        logger.error("Failed to leave game", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")