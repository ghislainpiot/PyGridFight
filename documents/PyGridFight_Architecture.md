# PyGridFight - Architecture Document (MVP)

**1. Introduction**
    1.1. Purpose of this Document
    1.2. Scope (MVP as defined in PRD, focusing on server-side architecture)
    1.3. Definitions, Acronyms, and Abbreviations
    1.4. References (Link to PRD: [`documents/PyGridFight_PRD.md`](documents/PyGridFight_PRD.md))
    1.5. Overview of the Document

**2. Architectural Goals and Constraints**
    2.1. Key Goals
        *   Real-time multiplayer for 2-4 players ([`documents/PyGridFight_PRD.md:19`](documents/PyGridFight_PRD.md:19), [`documents/PyGridFight_PRD.md:22`](documents/PyGridFight_PRD.md:22))
        *   API-first design for player interactions ([`documents/PyGridFight_PRD.md:54`](documents/PyGridFight_PRD.md:54))
        *   Support for spectator mode ([`documents/PyGridFight_PRD.md:157-166`](documents/PyGridFight_PRD.md:157-166))
        *   Independent testability of components
        *   Leverage FastAPI and its asynchronous capabilities
        *   Adherence to Domain-Driven Design principles
    2.2. Key Constraints
        *   Python as the primary programming language
        *   FastAPI framework for the API layer
        *   In-memory game state for MVP (no database persistence)
        *   WebSocket for client-server communication ([`documents/PyGridFight_PRD.md:51`](documents/PyGridFight_PRD.md:51))
        *   Game Engine logic integrated as a library within the FastAPI application

**3. System Overview**
    3.1. High-Level Architecture
        *   Brief description of the main components:
            *   FastAPI Application (hosting Game API & integrated Game Engine)
            *   Player Clients (interacting via WebSocket)
            *   Spectator Clients (interacting via WebSocket)
        *   Mermaid Diagram:
            ```mermaid
            graph TD
                A[Player Clients] -->|WebSocket JSON Messages| B(FastAPI Application)
                C[Spectator Clients] -->|WebSocket JSON Messages| B
                subgraph B [FastAPI Application / Game Server]
                    direction LR
                    D[WebSocket API Layer]
                    E[Game Engine (Integrated Library)]
                    D <--> E
                end
                style A fill:#f9f,stroke:#333,stroke-width:2px
                style C fill:#bbf,stroke:#333,stroke-width:2px
                style B fill:#ccf,stroke:#333,stroke-width:2px
                style D fill:#bfb,stroke:#333,stroke-width:2px
                style E fill:#fbf,stroke:#333,stroke-width:2px
            ```
    3.2. Component Responsibilities
        *   FastAPI Application: Handles WebSocket connections, message parsing/validation, hosts game logic, manages game sessions.
        *   Game Engine (Library): Core game rules, state management, turn processing.
        *   Player/Spectator Clients: UI rendering, sending actions (players), receiving state updates.

**4. Domain-Driven Design Approach**
    4.1. Overview of Bounded Contexts
        *   Brief explanation of DDD and Bounded Contexts.
        *   Chosen Bounded Contexts for MVP: `GameLifecycle`, `Gameplay`, `Scoring`.
    4.2. Bounded Context: `GameLifecycle`
        *   **Responsibilities**: Managing game creation, player connections (joining/leaving), starting/ending game sessions, tracking active games.
        *   **Potential Classes/Services**:
            *   `GameManager` (Service/Singleton):
                *   Attributes: `active_games: Dict[str, GameSessionRef]`, `player_connections: Dict[WebSocket, PlayerIdentity]`.
                *   Methods: `handle_connection(websocket, display_name)`, `handle_disconnection(websocket)`, `create_new_game(settings: GameSettings) -> GameSessionRef`, `find_game_for_player(player_identity: PlayerIdentity) -> Optional[GameSessionRef]`, `assign_player_to_game(player_identity: PlayerIdentity, game_id: str)`.
        *   **Key Value Objects**:
            *   `PlayerIdentity`: Attributes: `connection_id` (unique ID per WebSocket), `display_name`.
            *   `GameSettings`: Attributes: `grid_size: Coordinates`, `max_players: int`, `target_score: int`, `max_turns: int`.
            *   `GameSessionRef`: Attributes: `game_id: str` (identifier for a `GameSession` aggregate in the Gameplay context).
            *   `Coordinates`: Attributes: `x: int`, `y: int`. (Could reside in a `core.models` or `shared_kernel` module if used by multiple contexts directly).
    4.3. Bounded Context: `Gameplay`
        *   **Responsibilities**: Core game mechanics, turn management, avatar actions (move, collect, purchase), grid state (avatar positions, resource locations), resource spawning, direct consequences of actions on grid/avatars.
        *   **Key Aggregates & Entities**:
            *   `GameSession` (Aggregate Root):
                *   Attributes: `game_id: str`, `settings: GameSettings`, `players: Dict[str, Player]`, `grid: Grid`, `current_turn_player_id: Optional[str]`, `turn_number: int`, `game_status: GameStatusEnum`, `action_log: List[ActionRecord]`.
                *   Methods: `add_player(player_id: str, display_name: str)`, `remove_player(player_id: str)`, `start_game()`, `process_player_action(player_id: str, action: Action) -> List[GameEvent]`, `end_turn()`, `_spawn_resources()`, `_check_game_end_conditions()`, `get_full_state() -> dict`.
            *   `Player` (Entity within `GameSession`):
                *   Attributes: `player_id: str`, `display_name: str`, `avatars: Dict[str, Avatar]`, `currency: int` ([`documents/PyGridFight_PRD.md:62-63`](documents/PyGridFight_PRD.md:62-63)), `active_power_ups: List[ActivePowerUp]`.
                *   Methods: `can_purchase_avatar() -> bool`, `add_avatar(avatar: Avatar)`, `apply_action_to_avatar(avatar_id: str, action: Action)`.
            *   `Avatar` (Entity within `Player`):
                *   Attributes: `avatar_id: str`, `position: Coordinates`.
                *   Methods: `move(new_position: Coordinates, grid: Grid)`, `collect(cell: Cell) -> Optional[ResourceCollectedEvent]`.
            *   `Grid` (Entity, part of `GameSession`):
                *   Attributes: `size: Coordinates`, `cells: List[List[Cell]]`.
                *   Methods: `get_cell(coords: Coordinates) -> Cell`, `is_valid_move(current_pos: Coordinates, new_pos: Coordinates) -> bool`, `place_item(item: Union[Resource, Avatar], coords: Coordinates)`, `remove_item(coords: Coordinates)`, `get_random_empty_spawn_location() -> Coordinates`.
        *   **Key Value Objects**:
            *   `Cell`: Attributes: `coordinates: Coordinates`, `resource: Optional[Resource]`, `avatar_id: Optional[str]`.
            *   `Resource`: Attributes: `resource_id: str`, `resource_type: ResourceTypeEnum` (CURRENCY, POWERUP_SPEED), `value: Optional[int]`, `position: Coordinates`.
            *   `ActivePowerUp`: Attributes: `power_up_type: PowerUpTypeEnum`, `turns_remaining: int`.
            *   `Action` (Command, e.g., `MoveAction`, `CollectAction`, `PurchaseAvatarAction`):
                *   `MoveAction`: Attributes: `player_id: str`, `avatar_id: str`, `target_coordinates: Coordinates`.
                *   `CollectAction`: Attributes: `player_id: str`, `avatar_id: str`.
                *   `PurchaseAvatarAction`: Attributes: `player_id: str`, `spawn_coordinates: Coordinates`.
            *   `GameEvent` (e.g., `PlayerMovedEvent`, `ResourceCollectedEvent`, `AvatarPurchasedEvent`, `TurnChangedEvent`, `GameOverEvent`):
                *   Event-specific attributes, e.g., `PlayerMovedEvent(player_id: str, avatar_id: str, from_pos: Coordinates, to_pos: Coordinates)`.
            *   `ActionRecord`: Attributes: `player_id: str`, `action_details: dict`, `timestamp: datetime`.
            *   `GameStatusEnum`: (WAITING_FOR_PLAYERS, ACTIVE, FINISHED).
            *   `ResourceTypeEnum`: (CURRENCY, POWERUP_SPEED).
            *   `PowerUpTypeEnum`: (SPEED_BOOST).
    4.4. Bounded Context: `Scoring`
        *   **Responsibilities**: Tracking player scores, applying points from resource collection, determining victory conditions.
        *   **Potential Classes/Services**:
            *   `ScoreKeeper` (Service, could be part of `GameSession` or separate if logic is complex):
                *   Attributes: `player_scores: Dict[str, int]`.
                *   Methods: `add_points(player_id: str, points: int)`, `get_score(player_id: str) -> int`, `get_all_scores() -> Dict[str, int]`.
            *   `VictoryConditionChecker` (Service):
                *   Methods: `check_victory(game_settings: GameSettings, player_scores: Dict[str, int], current_turn: int) -> Optional[VictoryDetails]`.
        *   **Key Value Objects**:
            *   `VictoryDetails`: Attributes: `winning_player_id: Optional[str]`, `reason: VictoryReasonEnum` (TARGET_SCORE_REACHED, MAX_TURNS_REACHED, TIEBREAKER_HIGHEST_SCORE), `final_scores: Dict[str, int]`.
            *   `VictoryReasonEnum`: (TARGET_SCORE_REACHED, MAX_TURNS_REACHED, TIEBREAKER_HIGHEST_SCORE).
    4.5. Context Map (Illustrating interactions)
        ```mermaid
        graph TD
            GL[GameLifecycle Context] -->|Creates/Manages| GP[Gameplay Context (GameSession)]
            GP -->|Updates Player Scores via| S[Scoring Context]
            GP -->|Checks Victory Conditions via| S
            GP -->|Publishes Events/State| API[WebSocket API Layer]
            API -->|Connection Mgmt| GL
            API -->|Player Actions| GP

            subgraph Gameplay Context
                direction LR
                GameSess[GameSession AG]
                PlayerE[Player E]
                AvatarE[Avatar E]
                GridE[Grid E]
                CellVO[Cell VO]
                ResourceVO[Resource VO]
                ActionVO[Action VO]
                GameEventVO[GameEvent VO]
                GameSess --> PlayerE
                PlayerE --> AvatarE
                GameSess --> GridE
                GridE --> CellVO
                CellVO --> ResourceVO
            end

            subgraph Scoring Context
                ScoreKeeperSvc[ScoreKeeper Svc]
                VictoryCheckerSvc[VictoryConditionChecker Svc]
                VictoryDetailsVO[VictoryDetails VO]
                ScoreKeeperSvc --> VictoryDetailsVO
                VictoryCheckerSvc --> VictoryDetailsVO
            end

            subgraph GameLifecycle Context
                GameManagerSvc[GameManager Svc]
                PlayerIdentityVO[PlayerIdentity VO]
                GameSettingsVO[GameSettings VO]
            end

            style GL fill:#lightblue,stroke:#333,stroke-width:2px
            style GP fill:#lightgreen,stroke:#333,stroke-width:2px
            style S fill:#lightyellow,stroke:#333,stroke-width:2px
            style API fill:#lightcoral,stroke:#333,stroke-width:2px
        ```
    4.6. Proposed Module Structure (Python)
        *   A suggested Python package structure reflecting the Bounded Contexts:
            ```
            pygridfight_server/
            ├── main.py                 # FastAPI app instantiation, WebSocket endpoint
            ├── core/                   # Shared utilities, base classes, common enums, shared VOs (e.g. Coordinates)
            │   ├── __init__.py
            │   ├── enums.py            # GameStatusEnum, ResourceTypeEnum, PowerUpTypeEnum, VictoryReasonEnum
            │   ├── models.py           # Coordinates VO, other shared VOs
            │   └── utils.py
            ├── game_lifecycle/
            │   ├── __init__.py
            │   ├── manager.py          # GameManager service
            │   ├── models.py           # PlayerIdentity, GameSettings, GameSessionRef VOs
            │   └── exceptions.py
            ├── gameplay/
            │   ├── __init__.py
            │   ├── session.py          # GameSession aggregate root
            │   ├── player.py           # Player entity
            │   ├── avatar.py           # Avatar entity
            │   ├── grid.py             # Grid entity, Cell VO
            │   ├── resources.py        # Resource VO, ActivePowerUp VO
            │   ├── actions.py          # Action command VOs
            │   ├── events.py           # GameEvent VOs
            │   └── exceptions.py
            ├── scoring/
            │   ├── __init__.py
            │   ├── services.py         # ScoreKeeper, VictoryConditionChecker services
            │   ├── models.py           # VictoryDetails VO
            │   └── exceptions.py
            ├── api/
            │   ├── __init__.py
            │   ├── websockets.py       # WebSocket endpoint logic (could be in main.py for simple MVP)
            │   └── schemas.py          # Pydantic schemas for API messages (if not directly using domain VOs)
            └── tests/
                ├── test_game_lifecycle/
                ├── test_gameplay/
                └── test_scoring/
            ```
        *   Each context directory (`game_lifecycle`, `gameplay`, `scoring`) would contain its domain logic.
        *   The `core` directory can house truly shared elements like `Coordinates` or base enums if they are used across multiple contexts without specific contextual meaning.
        *   The `api` directory handles FastAPI-specific concerns.

**5. API Design (WebSocket)**
    5.1. Endpoint: `/ws` (Primary endpoint for players and spectators)
    5.2. Connection Management
        *   Player connection handshake (e.g., `{"type": "connect", "displayName": "PlayerX"}`).
        *   Spectator connection (e.g., `{"type": "spectate", "gameId": "optional_game_id"}`).
    5.3. Message Format: JSON (as per PRD [`documents/PyGridFight_PRD.md:147`](documents/PyGridFight_PRD.md:147))
        *   Key Action Messages (Player -> Server): `move`, `collect`, `purchase` (details from PRD [`documents/PyGridFight_PRD.md:154`](documents/PyGridFight_PRD.md:154)).
        *   Key State Update Messages (Server -> Client): Full game state, error messages (details from PRD [`documents/PyGridFight_PRD.md:149-150`](documents/PyGridFight_PRD.md:149-150)).
    5.4. State Synchronization: Server authoritative. Full state pushed after each validated action.
    5.5. Error Handling: Standardized error message format.

**6. Game Session Management (within FastAPI)**
    6.1. `GameSession` Objects: In-memory Python objects, each representing an active game.
    6.2. Tracking Active Games: A central dictionary (e.g., `active_games: Dict[str, GameSession]`) managed by the `GameLifecycle` context.
    6.3. Player to Game Mapping: How WebSocket connections are associated with `Player` objects within a `GameSession`.
    6.4. Game Lifecycle: Creation (on demand or by player action), active state, termination (e.g., victory, all players leave).

**7. Data Model (In-Memory Structures - further detail in Bounded Contexts)**
    *   This section can now be briefer, as much of the detail is moved into section 4. It can summarize the key entities like `Grid`, `Cell`, `Avatar`, `Resource`, `Player` and refer back to section 4 for detailed attributes and methods.

**8. Testability**
    8.1. Unit Testing: Focus on testing individual classes and methods within each Bounded Context (e.g., `Avatar.move()`, `ScoreKeeper.add_points()`, `VictoryConditionChecker.check_victory()`).
    8.2. Integration Testing: Testing interactions, e.g., `GameSession.process_player_action()` correctly updates `Player` state, `Grid` state, and `ScoreKeeper`.
    8.3. API Testing: Testing WebSocket communication, message validation, and state updates.

**9. Deployment View (MVP)**
    9.1. Single Process: The FastAPI application runs as a single Python process.
    9.2. Scalability Considerations (Brief): Mention that for MVP, it's single-instance; future scaling might involve multiple instances and a message bus/shared state if persistence is added.

**10. Future Considerations (Post-MVP)**
    *   Briefly touch upon how the chosen architecture might support items from PRD section 8 (e.g., new avatar types, AI opponents) by isolating changes within specific Bounded Contexts.
    *   Potential for introducing persistence.