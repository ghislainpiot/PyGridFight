"""Custom exceptions for PyGridFight."""


class PyGridFightError(Exception):
    """Base exception for PyGridFight."""

    def __init__(self, message: str, code: str = "UNKNOWN_ERROR") -> None:
        self.message = message
        self.code = code
        super().__init__(message)


class GameError(PyGridFightError):
    """Base exception for game-related errors."""
    pass


class GameNotFoundError(GameError):
    """Raised when a game is not found."""

    def __init__(self, game_id: str) -> None:
        super().__init__(f"Game with ID '{game_id}' not found", "GAME_NOT_FOUND")
        self.game_id = game_id


class GameFullError(GameError):
    """Raised when trying to join a full game."""

    def __init__(self, game_id: str) -> None:
        super().__init__(f"Game '{game_id}' is full", "GAME_FULL")
        self.game_id = game_id


class PlayerError(PyGridFightError):
    """Base exception for player-related errors."""
    pass


class PlayerNotFoundError(PlayerError):
    """Raised when a player is not found."""

    def __init__(self, player_id: str) -> None:
        super().__init__(f"Player with ID '{player_id}' not found", "PLAYER_NOT_FOUND")
        self.player_id = player_id


class InvalidActionError(PyGridFightError):
    """Raised when an invalid action is attempted."""

    def __init__(self, action: str, reason: str) -> None:
        super().__init__(f"Invalid action '{action}': {reason}", "INVALID_ACTION")
        self.action = action
        self.reason = reason


class ValidationError(PyGridFightError):
    """Raised when validation fails."""

    def __init__(self, field: str, value: str, reason: str) -> None:
        super().__init__(f"Validation failed for '{field}' with value '{value}': {reason}", "VALIDATION_ERROR")
        self.field = field
        self.value = value
        self.reason = reason