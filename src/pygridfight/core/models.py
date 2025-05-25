from dataclasses import dataclass, field


@dataclass(frozen=True)
class Coordinates:
    """
    Value object representing a 2D coordinate (x, y) on the grid.

    Attributes:
        x (int): The x-coordinate (column) on the grid.
        y (int): The y-coordinate (row) on the grid.

    Raises:
        TypeError: If x or y is not an integer.
    """
    x: int = field()
    y: int = field()

    def __post_init__(self):
        if not isinstance(self.x, int):
            raise TypeError(f"x must be an integer, got {type(self.x).__name__}")
        if not isinstance(self.y, int):
            raise TypeError(f"y must be an integer, got {type(self.y).__name__}")
