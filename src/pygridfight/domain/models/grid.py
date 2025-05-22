"""Grid domain model for PyGridFight."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from pygridfight.domain.enums import TerrainType
from pygridfight.domain.models.position import Position


@dataclass
class Cell:
    """Grid cell model."""

    position: Position
    terrain_type: TerrainType = TerrainType.EMPTY
    resource_id: Optional[str] = None
    avatar_id: Optional[str] = None

    @property
    def is_empty(self) -> bool:
        """Check if cell is empty."""
        return (self.terrain_type == TerrainType.EMPTY and
                self.resource_id is None and
                self.avatar_id is None)

    @property
    def is_passable(self) -> bool:
        """Check if cell can be moved through."""
        return self.terrain_type != TerrainType.WALL and self.avatar_id is None


@dataclass
class Grid:
    """Game grid model."""

    size: int
    cells: Dict[Tuple[int, int], Cell] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Initialize grid cells."""
        if not self.cells:
            self._initialize_cells()

    def _initialize_cells(self) -> None:
        """Initialize all grid cells."""
        for x in range(self.size):
            for y in range(self.size):
                position = Position(x, y)
                self.cells[(x, y)] = Cell(position=position)

    def get_cell(self, position: Position) -> Optional[Cell]:
        """Get cell at position."""
        return self.cells.get((position.x, position.y))

    def set_cell(self, position: Position, cell: Cell) -> None:
        """Set cell at position."""
        self.cells[(position.x, position.y)] = cell

    def is_valid_position(self, position: Position) -> bool:
        """Check if position is within grid bounds."""
        return 0 <= position.x < self.size and 0 <= position.y < self.size

    def is_position_passable(self, position: Position) -> bool:
        """Check if position can be moved to."""
        if not self.is_valid_position(position):
            return False

        cell = self.get_cell(position)
        return cell is not None and cell.is_passable

    def place_avatar(self, avatar_id: str, position: Position) -> bool:
        """Place avatar on grid."""
        if not self.is_position_passable(position):
            return False

        cell = self.get_cell(position)
        if cell:
            cell.avatar_id = avatar_id
            return True
        return False

    def remove_avatar(self, position: Position) -> None:
        """Remove avatar from grid."""
        cell = self.get_cell(position)
        if cell:
            cell.avatar_id = None

    def move_avatar(self, from_pos: Position, to_pos: Position) -> bool:
        """Move avatar from one position to another."""
        if not self.is_position_passable(to_pos):
            return False

        from_cell = self.get_cell(from_pos)
        to_cell = self.get_cell(to_pos)

        if from_cell and to_cell and from_cell.avatar_id:
            avatar_id = from_cell.avatar_id
            from_cell.avatar_id = None
            to_cell.avatar_id = avatar_id
            return True
        return False

    def get_neighbors(self, position: Position) -> List[Position]:
        """Get valid neighboring positions."""
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # N, S, W, E

        for dx, dy in directions:
            new_pos = Position(position.x + dx, position.y + dy)
            if self.is_valid_position(new_pos):
                neighbors.append(new_pos)

        return neighbors
from pydantic import BaseModel, Field, model_validator
from typing import List


class Grid(BaseModel):
    """
    Represents the game grid.

    Attributes:
        width (int): Number of columns in the grid.
        height (int): Number of rows in the grid.
    """
    width: int = Field(..., gt=0, description="Grid width (number of columns, must be > 0)")
    height: int = Field(..., gt=0, description="Grid height (number of rows, must be > 0)")

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
        return (
            0 <= position.x < self.width and
            0 <= position.y < self.height
        )

    def get_adjacent_positions(self, position: Position) -> List[Position]:
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