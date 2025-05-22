"""Custom middleware for PyGridFight FastAPI app."""

import structlog
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp, Receive, Scope, Send
from fastapi import Request as FastAPIRequest

from pygridfight.core.logging import get_logger

logger = get_logger(__name__)

class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware to add a unique request ID to each request."""

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log request and response details."""

    async def dispatch(self, request: Request, call_next):
        log = logger.bind(request_id=getattr(request.state, "request_id", None))
        log.info("Request started", method=request.method, url=str(request.url))
        response = await call_next(request)
        log.info("Request finished", status_code=response.status_code)
        return response

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware to catch unhandled exceptions and log them."""

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as exc:
            log = logger.bind(request_id=getattr(request.state, "request_id", None))
            log.error("Unhandled exception", error=str(exc))
            raise