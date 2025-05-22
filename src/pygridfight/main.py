"""FastAPI application entry point for PyGridFight."""

import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from pygridfight.api.middleware import (
    ErrorHandlingMiddleware,
    LoggingMiddleware,
    RequestIDMiddleware,
)
from pygridfight.core.config import get_settings
from pygridfight.core.exceptions import GameError, PlayerError
from pygridfight.core.logging import setup_logging

logger = structlog.get_logger()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    setup_logging()

    app = FastAPI(
        title="PyGridFight",
        description="A turn-based strategy game with WebSocket API",
        version="0.1.0",
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
    )

    # Add CORS middleware FIRST
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add custom middleware
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(ErrorHandlingMiddleware)

    # Register global exception handlers for custom exceptions
    @app.exception_handler(GameError)
    async def game_error_handler(request: Request, exc: GameError):
        logger.error(
            "GameError",
            error=str(exc),
            request_id=getattr(request.state, "request_id", None),
        )
        return JSONResponse(
            status_code=400,
            content={"error": "GameError", "message": str(exc)},
        )

    @app.exception_handler(PlayerError)
    async def player_error_handler(request: Request, exc: PlayerError):
        logger.error(
            "PlayerError",
            error=str(exc),
            request_id=getattr(request.state, "request_id", None),
        )
        return JSONResponse(
            status_code=400,
            content={"error": "PlayerError", "message": str(exc)},
        )

    # Startup/shutdown event handlers
    @app.on_event("startup")
    async def on_startup():
        logger.info("App startup", event="startup")

    @app.on_event("shutdown")
    async def on_shutdown():
        logger.info("App shutdown", event="shutdown")

    # Include routers
    from pygridfight.api.rest import router as rest_router

    app.include_router(rest_router)

    return app


app = create_app()


def main() -> None:
    """Main entry point for running the application."""
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "pygridfight.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_config=None,  # Use structlog instead
    )


if __name__ == "__main__":
    main()
