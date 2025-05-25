# PyGridFight - Roo Project Rules

This document outlines the agreed-upon rules and guidelines for the PyGridFight project. These rules are intended to ensure consistency, quality, and maintainability of the codebase. Adherence to these rules is expected from all contributors, including Roo.

## 1. General Project Standards

*   **1.1. Language:** All code, comments, and documentation must be in English.
*   **1.2. File Encoding:** All text files must use UTF-8 encoding.
*   **1.3. Naming Conventions:**
    *   Python modules: `lowercase_with_underscores` (e.g., `game_engine.py`).
    *   Python packages: `lowercase_with_underscores` (e.g., `game_lifecycle`).
    *   Classes: `CapWords` (e.g., `GameSession`, `PlayerIdentity`).
    *   Functions and methods: `lowercase_with_underscores` (e.g., `calculate_score()`, `handle_connection()`).
    *   Variables: `lowercase_with_underscores` (e.g., `active_games`, `player_id`).
    *   Constants: `UPPERCASE_WITH_UNDERSCORES` (e.g., `MAX_PLAYERS`, `DEFAULT_GRID_SIZE`).
*   **1.4. Documentation:**
    *   Public APIs (modules, classes, functions, methods) must have docstrings explaining their purpose, arguments, and return values.
    *   Complex logic or non-obvious decisions should be accompanied by inline comments.
    *   The `documents/PyGridFight_Architecture.md` and `documents/PyGridFight_PRD.md` should be kept up-to-date as the project evolves.

## 2. Test-Driven Development (TDD)

*   **2.1. Red-Green-Refactor:** All new functionality or bug fixes must start with a failing test (Red). Code is then written to make the test pass (Green). Finally, the code and tests can be refactored for clarity and efficiency (Refactor).
*   **2.2. Test Execution:** Tests must be run frequently during development using the command `uv run pytest`.
*   **2.3. Test Coverage:** All critical paths and business logic must be covered by tests.
*   **2.4. Test Granularity:** Write focused unit tests. Avoid testing multiple concerns in a single test case.

## 3. Architectural Principles

*   **3.1. Domain-Driven Design (DDD):**
    *   Adhere to the Bounded Contexts (`GameLifecycle`, `Gameplay`, `Scoring`) as defined in `documents/PyGridFight_Architecture.md`.
    *   Respect the responsibilities and boundaries of each Bounded Context.
    *   Utilize Aggregates, Entities, and Value Objects as appropriate within each context, following the patterns in `documents/PyGridFight_Architecture.md`.
*   **3.2. Module Structure:**
    *   Follow the proposed Python module structure outlined in `documents/PyGridFight_Architecture.md`.
    *   Place shared utilities, base classes, and common enums in the `core/` directory.
    *   Domain logic for each Bounded Context must reside within its respective package (e.g., `game_lifecycle/`, `gameplay/`, `scoring/`).
    *   API-specific concerns (WebSocket handling, schemas) should be in the `api/` directory.
*   **3.3. API-First Design:** Design and implement APIs with clear contracts, as specified in `documents/PyGridFight_Architecture.md`.
*   **3.4. Asynchronous Programming:** Leverage FastAPI's asynchronous capabilities for I/O-bound operations, especially for WebSocket communication, as per `documents/PyGridFight_Architecture.md`.
*   **3.5. In-Memory State:** For the MVP, game state will be managed in-memory. No database persistence layer is to be introduced without a new architectural decision, as per `documents/PyGridFight_Architecture.md`.

## 4. Testing Strategy

*   **4.1. Unit Testing:**
    *   Focus: Test individual classes, methods, and functions in isolation within each Bounded Context (e.g., `Avatar.move()`, `ScoreKeeper.add_points()`, `VictoryConditionChecker.check_victory()`).
    *   Mocking: Use mocks/stubs for external dependencies (other classes, services, or I/O) to ensure unit tests are fast and reliable.
    *   Location: Unit tests for a module should reside in a corresponding test file within the `tests/` directory, mirroring the application's structure (e.g., tests for `gameplay/avatar.py` in `tests/test_gameplay/test_avatar.py`).
*   **4.2. Integration Testing:**
    *   Focus: Test the interactions between components or services, e.g., how `GameSession.process_player_action()` correctly updates `Player` state, `Grid` state, and `ScoreKeeper`.
    *   Scope: Test interactions within a Bounded Context or between closely coupled Bounded Contexts (as defined by the Context Map in `documents/PyGridFight_Architecture.md`).
    *   Avoid over-mocking; allow real components to interact where feasible for the integration test's purpose.
*   **4.3. API Testing (WebSocket):**
    *   Focus: Test WebSocket communication, message validation (schemas), and state updates as perceived by a client.
    *   Scenarios: Cover connection handshake, player actions (move, collect, purchase), spectator mode, and error message handling.
    *   Tools: Utilize appropriate testing libraries for WebSocket clients if necessary.
*   **4.4. Test Data:** Use clear and representative test data. Avoid magic numbers or obscure values in tests; use named constants or descriptive variables.

## 5. Code Quality & Best Practices

*   **5.1. Readability:** Write code that is clear, concise, and easy to understand. Prioritize readability over overly clever or complex solutions.
*   **5.2. DRY (Don't Repeat Yourself):** Avoid duplicating code. Encapsulate common logic in functions, methods, or classes.
*   **5.3. YAGNI (You Ain't Gonna Need It):** Do not implement functionality that is not currently required by the PRD or architectural goals. Avoid premature generalization.
*   **5.4. KISS (Keep It Simple, Stupid):** Prefer simple solutions over complex ones. If a complex solution is necessary, ensure it is well-documented and justified.
*   **5.5. Premature Optimization:** Do not optimize code prematurely. Write clear, working code first, then optimize only if performance profiling indicates a bottleneck.
*   **5.6. Error Handling:**
    *   Handle potential errors gracefully. Use specific exceptions where appropriate (e.g., custom exceptions defined in `game_lifecycle/exceptions.py`).
    *   Provide clear error messages to users/clients, especially for API interactions.
*   **5.7. Immutability:** Prefer immutable objects (especially Value Objects) where practical to reduce side effects and simplify state management.
*   **5.8. Type Hinting:** All Python code must use `type hints` for function/method signatures and important variables to improve code clarity and enable static analysis.
*   **5.9. Linters & Formatters:** Ruff will be used. Adhere to project-defined linter configurations to ensure consistent code style.

## 6. Commit Messages and Version Control Practices

*   **6.1. Conventional Commits:** All commit messages must adhere to the Conventional Commits specification (e.g., `feat: add new avatar purchase endpoint`, `fix: correct score calculation for ties`, `docs: update architecture diagram for scoring`).
    *   Common types include: `feat`, `fix`, `build`, `chore`, `ci`, `docs`, `style`, `refactor`, `perf`, `test`.
*   **6.2. Atomic Commits:** Commits should be atomic and represent a single logical change. Avoid bundling unrelated changes into one commit.
*   **6.3. Test Before Commit:** All tests must pass (verified by running `uv run pytest`) before code is committed to the main development branch (trunk). Committing code that breaks tests is not allowed.
*   **6.4. Branching Strategy (Trunk-Based Development):** Development will primarily occur directly on the main branch (e.g., `main`). Short-lived feature branches may be used for larger changes or work that cannot be completed quickly, merging back to the trunk frequently (ideally multiple times a day, or at least daily). All code merged to the trunk must be production-ready and pass all tests.
*   **6.5. Meaningful Commit Messages:** Beyond the conventional commit type and scope, the commit message body (if present) should clearly explain the "what" and "why" of the change, not just the "how".

## 7. Dependency Management Rules

*   **7.1. `uv` for Dependency Management:** All Python package dependencies must be managed using the `uv` command-line tool (e.g., `uv pip install <package>`, `uv pip uninstall <package>`).
*   **7.2. No Direct Editing of Dependency Files for Management:** Manually editing files like `pyproject.toml` (specifically the `[project.dependencies]` or `[project.optional-dependencies]` sections) or `requirements.txt` (if used) for the purpose of adding, removing, or updating dependencies is forbidden. These files should only be modified by the `uv` tool itself or for non-dependency-management configuration.
*   **7.3. Dependency Pinning & Lock Files:** Dependencies should be pinned to specific versions in `pyproject.toml` (e.g., `package_name=="1.2.3"` or using compatible release specifiers like `package_name>=1.2.0,<1.3.0`) to ensure a degree of stability and control over updates. A lock file (e.g., `requirements.lock.txt` or `uv.lock`, depending on the chosen `uv` workflow) should be generated and committed to the repository. This lock file must only be updated when dependencies are intentionally added, removed, or upgraded. It should not be updated automatically on every commit if the underlying resolved dependencies have not changed.
*   **7.4. Review New Dependencies:** Adding new dependencies should be done thoughtfully. Consider the impact on project size, security, and maintenance. Discuss with the team if a new dependency is significant or controversial.
*   **7.5. Keep Dependencies Updated:** Regularly review and update dependencies to their latest stable and compatible versions to incorporate bug fixes, security patches, and new features. Test thoroughly after updates.