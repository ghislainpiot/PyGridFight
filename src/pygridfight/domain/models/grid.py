"""Grid domain model for PyGridFight."""

from dataclasses import dataclass

from pydantic import BaseModel, Field, model_validator

from pygridfight.domain.enums import TerrainType
from pygridfight.domain.models.position import Position


@dataclass
class Cell:
    """Grid cell model."""

    position: Position
    terrain_type: TerrainType = TerrainType.EMPTY
    resource_id: str | None = None
    avatar_id: str | None = None

    @property
    def is_empty(self) -> bool:
        """Check if cell is empty."""
        return (
            self.terrain_type == TerrainType.EMPTY
            and self.resource_id is None
            and self.avatar_id is None
        )

    @property
    def is_passable(self) -> bool:
        """Check if cell can be moved through."""
        return self.terrain_type != TerrainType.WALL and self.avatar_id is None


class Grid(BaseModel):
    """
    Represents the game grid.

    Attributes:
        width (int): Number of columns in the grid.
        height (int): Number of rows in the grid.
    """

    width: int = Field(
        ..., gt=0, description="Grid width (number of columns, must be > 0)"
    )
    height: int = Field(
        ..., gt=0, description="Grid height (number of rows, must be > 0)"
    )

    @model_validator(mode="after")
    def check_dimensions(self):
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Grid width and height must be positive integers.")
        return self

    def is_valid_position(self, position: Position) -> bool:
        """
        Check if a position is within the grid bounds.

        Args:
            position (Position): The position to check.

        Returns:
            bool: True if position is within bounds, False otherwise.
        """
        return 0 <= position.x < self.width and 0 <= position.y < self.height

    def get_adjacent_positions(self, position: Position) -> list[Position]:
        """
        Get all cardinally adjacent positions (up, down, left, right) within grid bounds.

        Args:
            position (Position): The reference position.

        Returns:
            List[Position]: List of valid adjacent positions.
        """
        deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        adjacents = []
        for dx, dy in deltas:
            new_x, new_y = position.x + dx, position.y + dy
            candidate = Position(x=new_x, y=new_y)
            if self.is_valid_position(candidate):
                adjacents.append(candidate)
        return adjacents

    @staticmethod
    def distance(pos1: Position, pos2: Position) -> int:
        """
        Compute the Manhattan distance between two positions.

        Args:
            pos1 (Position): The first position.
            pos2 (Position): The second position.

        Returns:
            int: The Manhattan distance.
        """
        return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y)
