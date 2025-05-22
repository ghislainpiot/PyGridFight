"""FastAPI application entry point for PyGridFight."""

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pygridfight.core.config import get_settings
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

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

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