"""REST API endpoints for PyGridFight."""

from fastapi import APIRouter, HTTPException, status
import structlog
from fastapi.responses import JSONResponse

from pygridfight.core.exceptions import GameError, PlayerError

logger = structlog.get_logger(__name__)

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
async def list_games() -> dict:
    """List all available games."""
    # TODO: Implement game listing
    return {"games": []}


@router.post("/games")
async def create_game() -> dict:
    """Create a new game."""
    # TODO: Implement game creation
    return {"game_id": "placeholder", "status": "created"}


@router.get("/games/{game_id}")
async def get_game(game_id: str) -> dict:
    """Get game details."""
    # TODO: Implement game retrieval
    try:
        return {"game_id": game_id, "status": "placeholder"}
    except GameError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "code": e.code}
        )


@router.post("/games/{game_id}/join")
async def join_game(game_id: str) -> dict:
    """Join an existing game."""
    # TODO: Implement game joining
    try:
        return {"game_id": game_id, "player_id": "placeholder", "status": "joined"}
    except GameError as e:
        if isinstance(e, GameError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": e.message, "code": e.code}
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "code": e.code}
        )


@router.delete("/games/{game_id}/leave")
async def leave_game(game_id: str) -> dict:
    """Leave a game."""
    # TODO: Implement game leaving
    try:
        return {"game_id": game_id, "status": "left"}
    except (GameError, PlayerError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "code": e.code}
        )