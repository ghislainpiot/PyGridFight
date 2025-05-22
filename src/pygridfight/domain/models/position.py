"""Position domain model for PyGridFight."""

from pydantic import BaseModel, Field


class Position(BaseModel):
    """
    Represents a position on the grid.

    Attributes:
        x (int): The x-coordinate (column).
        y (int): The y-coordinate (row).
    """

    x: int = Field(..., description="X coordinate (column)")
    y: int = Field(..., description="Y coordinate (row)")

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if not isinstance(other, Position):
            return NotImplemented
        return self.x == other.x and self.y == other.y
