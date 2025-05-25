from typing import Dict
from pygridfight.gameplay.session import GameSession
from pygridfight.api.schemas import (
    GameStateSchema,
    PlayerSchema,
    AvatarSchema,
    GridSchema,
    CellSchema,
)
from pygridfight.core.models import Coordinates


def convert_game_session_to_schema(session: GameSession) -> GameStateSchema:
    """
    Convert a GameSession domain object to a GameStateSchema for API responses.

    Args:
        session (GameSession): The game session to convert.

    Returns:
        GameStateSchema: The API schema representation of the game state.
    """
    # Convert grid cells: Dict[Coordinates, Cell] -> Dict[str, CellSchema]
    grid_schema_cells: Dict[str, CellSchema] = {
        f"{coords.x},{coords.y}": CellSchema.model_validate(cell)
        for coords, cell in session.grid.cells.items()
    }
    grid_schema = GridSchema(
        size=session.grid.size,
        cells=grid_schema_cells
    )
    # Convert avatars
    avatar_schemas = [
        AvatarSchema.model_validate(avatar)
        for avatar in session.player.avatars
    ]
    # Player score
    player_score = session.score_keeper.get_score(session.player.player_id)
    player_schema = PlayerSchema(
        player_id=session.player.player_id,
        display_name=session.player.display_name,
        avatars=avatar_schemas,
        currency=session.player.currency,
        score=player_score if player_score is not None else 0
    )
    return GameStateSchema(
        session_id=session.session_id,
        status=session.status,
        current_turn=session.current_turn,
        grid=grid_schema,
        players=[player_schema],
        target_score=session.target_score,
        winner=session.winner
    )