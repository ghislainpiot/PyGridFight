"""Logging configuration for PyGridFight."""

import logging
import sys
import structlog
import contextvars
from functools import wraps
from contextlib import contextmanager
from typing import Any, Callable

from src.pygridfight.core.config import get_server_settings

# Context variable for correlation ID
_correlation_id_ctx = contextvars.ContextVar("correlation_id", default=None)

def _add_correlation_id(logger, method_name, event_dict):
    cid = _correlation_id_ctx.get()
    if cid is not None:
        event_dict["correlation_id"] = cid
    return event_dict

def setup_logging() -> None:
    """Set up structured logging for the application."""
    settings = get_server_settings()
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
    log_format = getattr(settings, "log_format", "json")

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
    )

    processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        _add_correlation_id,
    ]

    if log_format == "json":
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

def get_logger(name: str = __name__) -> structlog.BoundLogger:
    """Get a structured logger instance."""
    return structlog.get_logger(name)

@contextmanager
def with_correlation_id(correlation_id: str):
    """Context manager to set correlation ID for logs."""
    token = _correlation_id_ctx.set(correlation_id)
    try:
        yield
    finally:
        _correlation_id_ctx.reset(token)

def log_with_correlation_id(func: Callable) -> Callable:
    """Decorator to propagate correlation ID into function logs."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@contextmanager
def with_request_context(request: Any):
    """
    Context manager to extract correlation ID from FastAPI request.state.
    """
    correlation_id = getattr(getattr(request, "state", None), "correlation_id", None)
    if correlation_id:
        with with_correlation_id(correlation_id):
            yield
    else:
        yield