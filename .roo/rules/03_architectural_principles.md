# Architectural Principles

## Domain-Driven Design (DDD)
- Adhere to the Bounded Contexts (`GameLifecycle`, `Gameplay`, `Scoring`) as defined in `documents/PyGridFight_Architecture.md`
- Respect the responsibilities and boundaries of each Bounded Context
- Utilize Aggregates, Entities, and Value Objects as appropriate within each context

## Module Structure
- Follow the proposed Python module structure outlined in `documents/PyGridFight_Architecture.md`
- Place shared utilities, base classes, and common enums in the `core/` directory
- Domain logic for each Bounded Context must reside within its respective package (e.g., `game_lifecycle/`, `gameplay/`, `scoring/`)
- API-specific concerns (WebSocket handling, schemas) should be in the `api/` directory

## Design Principles
- Design and implement APIs with clear contracts, as specified in `documents/PyGridFight_Architecture.md`
- Leverage FastAPI's asynchronous capabilities for I/O-bound operations, especially for WebSocket communication
- For the MVP, game state will be managed in-memory. No database persistence layer is to be introduced without a new architectural decision