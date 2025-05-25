# Code Quality & Best Practices

## Core Principles
- Write code that is clear, concise, and easy to understand
- DRY (Don't Repeat Yourself): Avoid duplicating code; encapsulate common logic in functions, methods, or classes
- YAGNI (You Ain't Gonna Need It): Do not implement functionality that is not currently required
- KISS (Keep It Simple, Stupid): Prefer simple solutions over complex ones
- Do not optimize code prematurely; write clear, working code first

## Error Handling
- Handle potential errors gracefully using specific exceptions where appropriate
- Provide clear error messages to users/clients, especially for API interactions
- Use custom exceptions defined in appropriate modules (e.g., `game_lifecycle/exceptions.py`)

## Code Standards
- Prefer immutable objects (especially Value Objects) where practical to reduce side effects
- All Python code must use type hints for function/method signatures and important variables
- Use Ruff for linting and formatting; adhere to project-defined configurations for consistent code style