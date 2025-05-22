# PyGridFight

A turn-based strategy game with WebSocket API built with FastAPI and Python 3.12+.

## Overview

PyGridFight is a multiplayer grid-based strategy game where players control avatars, collect resources, and engage in combat. The game features real-time communication through WebSockets and a REST API for game management.

## Features

- **Multiplayer Support**: Up to 8 players per game
- **Real-time Communication**: WebSocket-based game updates
- **Grid-based Gameplay**: Strategic movement and positioning
- **Resource Management**: Collect and manage various resources
- **Combat System**: Turn-based combat mechanics
- **RESTful API**: Complete API for game and player management

## Technology Stack

- **Python 3.12+**: Modern Python with type hints
- **FastAPI**: High-performance web framework
- **Pydantic v2**: Data validation and serialization
- **WebSockets**: Real-time bidirectional communication
- **structlog**: Structured logging
- **pytest**: Testing framework
- **ruff**: Code formatting and linting
- **mypy**: Static type checking

## Quick Start

### Prerequisites

- Python 3.12 or higher
- uv package manager
- devenv (optional, for development environment)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd PyGridFight
```

2. Set up the development environment:
```bash
# Using devenv (recommended)
devenv shell

# Or using uv directly
uv pip install -e ".[dev]"
```

3. Install pre-commit hooks:
```bash
pre-commit install
```

### Running the Application

```bash
# Using make
make run

# Or directly with uvicorn
uvicorn pygridfight.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000` with interactive documentation at `http://localhost:8000/docs`.

## Development

### Available Commands

```bash
make help           # Show available commands
make install        # Install dependencies
make format         # Format code with ruff
make lint           # Lint code with ruff and mypy
make test           # Run all tests
make test-unit      # Run unit tests only
make test-integration # Run integration tests only
make run            # Run development server
make clean          # Clean up temporary files
```

### Project Structure

```
PyGridFight/
├── src/pygridfight/        # Main application code
│   ├── api/                # API layer (REST & WebSocket)
│   ├── core/               # Core utilities (config, logging, exceptions)
│   ├── domain/             # Domain models and business logic
│   ├── services/           # Application services
│   └── infrastructure/     # Infrastructure layer
├── tests/                  # Test suite
│   ├── unit/              # Unit tests
│   └── integration/       # Integration tests
├── docs/                  # Documentation
├── scripts/               # Utility scripts
└── pyproject.toml         # Project configuration
```

### Code Quality

This project follows strict code quality standards:

- **Type Safety**: Full type hints with mypy checking
- **Code Style**: Enforced with ruff formatter
- **Linting**: Comprehensive linting with ruff
- **Testing**: High test coverage with pytest
- **Pre-commit Hooks**: Automated quality checks

### Configuration

The application can be configured using environment variables with the `PYGRIDFIGHT_` prefix:

- `PYGRIDFIGHT_HOST`: Server host (default: 0.0.0.0)
- `PYGRIDFIGHT_PORT`: Server port (default: 8000)
- `PYGRIDFIGHT_DEBUG`: Enable debug mode (default: False)
- `PYGRIDFIGHT_LOG_LEVEL`: Logging level (default: INFO)

## API Documentation

Once the server is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

## Testing

```bash
# Run all tests
make test

# Run specific test types
make test-unit
make test-integration

# Run tests with coverage
pytest tests/ -v --cov=src --cov-report=html
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

Please ensure all tests pass and code follows the project's style guidelines.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Architecture

PyGridFight follows a clean architecture pattern with clear separation of concerns:

- **API Layer**: Handles HTTP requests and WebSocket connections
- **Domain Layer**: Contains business logic and domain models
- **Service Layer**: Orchestrates business operations
- **Infrastructure Layer**: Manages external dependencies and state

For detailed architecture documentation, see the `docs/architecture/` directory.