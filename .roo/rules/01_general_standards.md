# General Project Standards

## Language and Encoding
- All code, comments, and documentation must be in English
- All text files must use UTF-8 encoding

## Naming Conventions
- Python modules: `lowercase_with_underscores` (e.g., `game_engine.py`)
- Python packages: `lowercase_with_underscores` (e.g., `game_lifecycle`)
- Classes: `CapWords` (e.g., `GameSession`, `PlayerIdentity`)
- Functions and methods: `lowercase_with_underscores` (e.g., `calculate_score()`, `handle_connection()`)
- Variables: `lowercase_with_underscores` (e.g., `active_games`, `player_id`)
- Constants: `UPPERCASE_WITH_UNDERSCORES` (e.g., `MAX_PLAYERS`, `DEFAULT_GRID_SIZE`)

## Documentation Requirements
- Public APIs (modules, classes, functions, methods) must have docstrings explaining their purpose, arguments, and return values
- Complex logic or non-obvious decisions should be accompanied by inline comments
- Keep `documents/PyGridFight_Architecture.md` and `documents/PyGridFight_PRD.md` up-to-date as the project evolves