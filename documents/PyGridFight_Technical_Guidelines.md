# PyGridFight Technical Guidelines for AI Agents

## Overview
This document provides technical guidelines, coding standards, and best practices for AI agents implementing PyGridFight tasks. Following these guidelines ensures consistency, maintainability, and quality across the codebase.

## Table of Contents
1. [General Principles](#general-principles)
2. [Python Coding Standards](#python-coding-standards)
3. [Project Structure Guidelines](#project-structure-guidelines)
4. [Testing Guidelines](#testing-guidelines)
5. [Commit Convention](#commit-convention)
6. [Error Handling](#error-handling)
7. [Documentation Standards](#documentation-standards)
8. [Performance Considerations](#performance-considerations)
9. [Security Best Practices](#security-best-practices)
10. [Code Review Checklist](#code-review-checklist)

## General Principles

### Core Development Principles
- **KISS (Keep It Simple, Stupid)**: Start with the simplest solution that works
- **DRY (Don't Repeat Yourself)**: Extract common functionality into reusable components
- **YAGNI (You Aren't Gonna Need It)**: Don't add functionality until it's needed
- **SOLID Principles**: Follow object-oriented design principles where applicable

### Development Workflow
1. Read and understand the task requirements completely
2. Write tests first (TDD approach) or alongside implementation
3. Implement the simplest working solution
4. Refactor for clarity and efficiency
5. Ensure all tests pass
6. Document your code
7. Create meaningful commits

## Python Coding Standards

### Style Guide
Follow PEP 8 with these specific conventions:

```python
# File naming: lowercase with underscores
game_manager.py

# Class naming: PascalCase
class GameManager:
    pass

# Function/method naming: lowercase with underscores
def calculate_distance(pos1: Position, pos2: Position) -> int:
    pass

# Constants: UPPERCASE with underscores
MAX_PLAYERS = 4
DEFAULT_GRID_SIZE = 8

# Private methods/attributes: single underscore prefix
def _validate_position(self, position: Position) -> bool:
    pass
```

### Type Hints
Always use type hints for function parameters and return values:

```python
from typing import Optional, List, Dict, Union
from datetime import datetime

def process_action(
    game_id: str,
    player_id: str,
    action: ActionMessage,
    timestamp: Optional[datetime] = None
) -> Dict[str, Any]:
    """Process a player action and return the updated game state."""
    pass
```

### Imports
Organize imports in this order:
1. Standard library imports
2. Third-party imports
3. Local application imports

```python
# Standard library
import json
from datetime import datetime
from typing import List, Optional

# Third-party
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel, Field
import structlog

# Local application
from pygridfight.domain.models import Game, Player
from pygridfight.core.exceptions import GameNotFoundException
```

### Async/Await Best Practices
```python
# Good: Use async for I/O operations
async def get_game(self, game_id: str) -> Optional[Game]:
    async with self._lock:
        return self._games.get(game_id)

# Good: Use asyncio.gather for concurrent operations
results = await asyncio.gather(
    self.update_game(game_id, game),
    self.broadcast_state(game_id),
    return_exceptions=True
)
```

## Project Structure Guidelines

### Module Organization
```
src/pygridfight/
├── api/              # API layer (REST, WebSocket handlers)
├── core/             # Core utilities (config, logging, exceptions)
├── domain/           # Domain models and business logic
├── services/         # Business services and orchestration
└── infrastructure/   # External integrations and persistence
```

### File Naming Conventions
- Domain models: `{entity}.py` (e.g., `player.py`, `game.py`)
- Services: `{entity}_service.py` (e.g., `game_service.py`)
- API handlers: `{feature}.py` (e.g., `websocket.py`, `rest.py`)
- Tests: `test_{module}.py` (e.g., `test_game_engine.py`)

## Testing Guidelines

### Test Structure
```python
# tests/unit/test_game_engine.py
import pytest
from pygridfight.services.game_engine import GameEngine
from pygridfight.domain.models import Game, Player, Position

class TestGameEngine:
    """Test suite for GameEngine service."""

    @pytest.fixture
    def game_engine(self):
        """Create a GameEngine instance for testing."""
        return GameEngine()

    @pytest.fixture
    def sample_game(self):
        """Create a sample game for testing."""
        return Game(
            id="test-game-1",
            grid_size=8,
            max_players=4
        )

    async def test_move_avatar_valid(self, game_engine, sample_game):
        """Test that avatar can move to adjacent empty cell."""
        # Arrange
        player = Player(id="player-1", display_name="Test Player")
        avatar = game_engine.create_avatar(player.id, Position(x=0, y=0))

        # Act
        result = await game_engine.move_avatar(
            game=sample_game,
            avatar_id=avatar.id,
            new_position=Position(x=1, y=0)
        )

        # Assert
        assert result.success is True
        assert avatar.position == Position(x=1, y=0)

    async def test_move_avatar_invalid_not_adjacent(self, game_engine, sample_game):
        """Test that avatar cannot move to non-adjacent cell."""
        # Test implementation...
```

### Testing Best Practices

1. **Test Naming**: Use descriptive names that explain what is being tested
   ```python
   # Good
   def test_player_cannot_join_full_game():

   # Bad
   def test_join_game_2():
   ```

2. **AAA Pattern**: Arrange, Act, Assert
   ```python
   def test_collect_resource():
       # Arrange
       game = create_test_game()
       resource = create_resource(position=Position(x=2, y=2))

       # Act
       result = game.collect_resource(player_id="p1", position=Position(x=2, y=2))

       # Assert
       assert result.points_gained == 3
       assert resource.id not in game.resources
   ```

3. **Fixtures**: Use pytest fixtures for reusable test data
   ```python
   @pytest.fixture
   def game_with_players():
       game = Game(id="test-1")
       game.add_player(Player(id="p1", display_name="Player 1"))
       game.add_player(Player(id="p2", display_name="Player 2"))
       return game
   ```

4. **Parametrized Tests**: Test multiple scenarios efficiently
   ```python
   @pytest.mark.parametrize("start_pos,end_pos,expected", [
       (Position(0, 0), Position(1, 0), True),   # Valid horizontal move
       (Position(0, 0), Position(0, 1), True),   # Valid vertical move
       (Position(0, 0), Position(2, 0), False),  # Invalid: too far
       (Position(0, 0), Position(1, 1), False),  # Invalid: diagonal
   ])
   def test_is_valid_move(start_pos, end_pos, expected):
       assert is_adjacent(start_pos, end_pos) == expected
   ```

5. **Mock External Dependencies**
   ```python
   from unittest.mock import AsyncMock, patch

   @patch('pygridfight.infrastructure.events.EventManager')
   async def test_game_end_notification(mock_event_manager):
       mock_event_manager.emit = AsyncMock()

       # Test game end logic
       await game_engine.end_game(game_id="test-1")

       # Verify event was emitted
       mock_event_manager.emit.assert_called_once_with(
           "game_ended",
           game_id="test-1"
       )
   ```

### Test Coverage Requirements
- Aim for minimum 80% code coverage
- Critical paths (game logic, combat, scoring) should have 100% coverage
- Use `pytest-cov` to measure coverage:
  ```bash
  pytest --cov=pygridfight --cov-report=html
  ```

## Commit Convention

### Conventional Commits Format
Follow the Conventional Commits specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, missing semicolons, etc.)
- **refactor**: Code refactoring without changing functionality
- **test**: Adding or modifying tests
- **chore**: Maintenance tasks, dependency updates
- **perf**: Performance improvements

### Examples
```bash
# Feature commit
feat(game): implement avatar movement validation

Add validation logic for avatar movement including:
- Adjacent cell checking
- Grid boundary validation
- Collision detection with other avatars

# Bug fix
fix(websocket): handle disconnection during game action

Properly clean up player state when WebSocket disconnects
during action processing to prevent orphaned connections.

Fixes #123

# Test commit
test(combat): add unit tests for combat resolution

Add comprehensive test coverage for combat system including:
- Attack validation
- Combat resolution
- Avatar destruction
- State updates after combat

# Refactor commit
refactor(api): extract message validation to separate module

Move all Pydantic message schemas to dedicated module
for better organization and reusability.
```

### Commit Best Practices
1. Keep commits atomic (one logical change per commit)
2. Write clear, descriptive commit messages
3. Reference issue numbers when applicable
4. Use present tense ("add feature" not "added feature")
5. Keep subject line under 50 characters
6. Wrap body at 72 characters

## Error Handling

### Custom Exceptions
```python
# pygridfight/core/exceptions.py
class PyGridFightException(Exception):
    """Base exception for all game errors."""
    pass

class GameNotFoundException(PyGridFightException):
    """Raised when game doesn't exist."""
    def __init__(self, game_id: str):
        self.game_id = game_id
        super().__init__(f"Game not found: {game_id}")

class InvalidActionException(PyGridFightException):
    """Raised when action is invalid."""
    def __init__(self, action: str, reason: str):
        self.action = action
        self.reason = reason
        super().__init__(f"Invalid action '{action}': {reason}")
```

### Error Handling Patterns
```python
# Service layer
async def move_avatar(self, game_id: str, avatar_id: str, position: Position):
    try:
        game = await self.get_game(game_id)
        if not game:
            raise GameNotFoundException(game_id)

        avatar = game.get_avatar(avatar_id)
        if not avatar:
            raise InvalidActionException("move", "Avatar not found")

        # Perform move...

    except PyGridFightException:
        # Re-raise domain exceptions
        raise
    except Exception as e:
        # Log unexpected errors
        logger.error("Unexpected error in move_avatar", error=str(e))
        raise

# API layer
@app.exception_handler(PyGridFightException)
async def handle_game_exception(request: Request, exc: PyGridFightException):
    return JSONResponse(
        status_code=400,
        content={
            "error": exc.__class__.__name__,
            "message": str(exc)
        }
    )
```

## Documentation Standards

### Docstrings
Use Google-style docstrings:

```python
def calculate_damage(attacker: Avatar, defender: Avatar, modifiers: List[str]) -> int:
    """Calculate damage dealt in combat.

    Args:
        attacker: The attacking avatar
        defender: The defending avatar
        modifiers: List of active combat modifiers

    Returns:
        The amount of damage dealt

    Raises:
        InvalidCombatException: If combat is not valid

    Example:
        >>> damage = calculate_damage(avatar1, avatar2, ["critical_hit"])
        >>> print(damage)
        2
    """
    pass
```

### API Documentation
```python
@router.post("/games", response_model=GameResponse)
async def create_game(
    settings: GameSettings = Body(..., example={
        "grid_size": 8,
        "max_players": 4,
        "target_score": 20
    })
) -> GameResponse:
    """Create a new game instance.

    Creates a new game with the specified settings and returns
    the game ID and initial state.
    """
    pass
```

### README Documentation
Each module should have a README explaining:
- Purpose and responsibilities
- Key classes and functions
- Usage examples
- Dependencies

## Performance Considerations

### Optimization Guidelines
1. **Profile First**: Don't optimize without profiling
   ```python
   import cProfile
   import pstats

   profiler = cProfile.Profile()
   profiler.enable()
   # Code to profile
   profiler.disable()
   stats = pstats.Stats(profiler).sort_stats('cumulative')
   stats.print_stats()
   ```

2. **Async Best Practices**
   ```python
   # Good: Concurrent operations
   await asyncio.gather(
       self.update_player(player1),
       self.update_player(player2),
       self.broadcast_state()
   )

   # Bad: Sequential operations
   await self.update_player(player1)
   await self.update_player(player2)
   await self.broadcast_state()
   ```

3. **Caching Strategy**
   ```python
   from functools import lru_cache

   @lru_cache(maxsize=128)
   def calculate_distance(pos1: tuple, pos2: tuple) -> int:
       """Cache distance calculations for frequently accessed positions."""
       x1, y1 = pos1
       x2, y2 = pos2
       return abs(x2 - x1) + abs(y2 - y1)
   ```

## Security Best Practices

### Input Validation
```python
# Always validate user input
class MoveAction(BaseModel):
    avatar_id: str = Field(..., min_length=1, max_length=50)
    position: Position

    @field_validator('avatar_id')
    def validate_avatar_id(cls, v):
        if not v.replace('-', '').isalnum():
            raise ValueError('Invalid avatar ID format')
        return v
```

### Rate Limiting
```python
from fastapi import HTTPException
from collections import defaultdict
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_requests: int = 100, window: timedelta = timedelta(minutes=1)):
        self.max_requests = max_requests
        self.window = window
        self.requests = defaultdict(list)

    async def check_rate_limit(self, client_id: str):
        now = datetime.now()
        # Clean old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < self.window
        ]

        if len(self.requests[client_id]) >= self.max_requests:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")

        self.requests[client_id].append(now)
```

## Code Review Checklist

Before submitting code, ensure:

### Functionality
- [ ] Code implements the required functionality
- [ ] All acceptance criteria are met
- [ ] Edge cases are handled

### Code Quality
- [ ] Code follows PEP 8 style guide
- [ ] Type hints are used consistently
- [ ] No code duplication (DRY principle)
- [ ] Functions are small and focused (single responsibility)
- [ ] Variable and function names are descriptive

### Testing
- [ ] Unit tests cover all new functionality
- [ ] Tests follow AAA pattern
- [ ] Edge cases are tested
- [ ] All tests pass
- [ ] Code coverage meets requirements (80%+)

### Documentation
- [ ] All functions have docstrings
- [ ] Complex logic is commented
- [ ] API endpoints are documented
- [ ] README is updated if needed

### Performance & Security
- [ ] No obvious performance issues
- [ ] Async operations are used appropriately
- [ ] User input is validated
- [ ] No sensitive data in logs

### Git
- [ ] Commits follow conventional commits format
- [ ] Commit messages are clear and descriptive
- [ ] No debugging code or print statements

---

## Quick Reference

### Common Patterns

**Dependency Injection in FastAPI:**
```python
async def get_game_manager() -> GameStateManager:
    return game_state_manager

@router.post("/games/{game_id}/actions")
async def process_action(
    game_id: str,
    action: ActionMessage,
    manager: GameStateManager = Depends(get_game_manager)
):
    return await manager.process_action(game_id, action)
```

**Structured Logging:**
```python
logger = structlog.get_logger()

logger.info(
    "action_processed",
    game_id=game_id,
    player_id=player_id,
    action_type=action.type,
    duration_ms=duration
)
```

**WebSocket Message Handling:**
```python
async def handle_message(websocket: WebSocket, message: dict):
    try:
        action = ActionMessage(**message)
        result = await process_action(action)
        await websocket.send_json(result.dict())
    except ValidationError as e:
        await websocket.send_json({
            "type": "error",
            "message": "Invalid message format",
            "details": e.errors()
        })
```

---

**Document Version**: 1.0
**Last Updated**: January 2025
**Applies to**: PyGridFight Implementation Tasks