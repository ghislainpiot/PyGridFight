from typing import Dict, Optional
from pygridfight.core.models import Coordinates
from pygridfight.gameplay.models import Cell
from pygridfight.gameplay.resources import Resource

class Grid:
    """
    Entity representing the game grid, managing a collection of cells and providing grid operations.

    Attributes:
        size (int): The size of the grid (number of rows and columns; grid is size x size).
        cells (Dict[Coordinates, Cell]): Dictionary mapping coordinates to Cell objects.
    """

    def __init__(self, size: int) -> None:
        """
        Initialize the grid with the given size, creating a Cell for each coordinate.

        Args:
            size (int): The size of the grid (number of rows and columns).
        """
        self.size: int = size
        self.cells: Dict[Coordinates, Cell] = {}
        for x in range(size):
            for y in range(size):
                coords = Coordinates(x=x, y=y)
                self.cells[coords] = Cell(coordinates=coords)

    def get_cell(self, coordinates: Coordinates) -> Cell:
        """
        Retrieve the cell at the given coordinates.

        Args:
            coordinates (Coordinates): The coordinates of the cell to retrieve.

        Returns:
            Cell: The cell at the specified coordinates.

        Raises:
            ValueError: If the coordinates are out of bounds.
        """
        if not self.is_valid_coordinates(coordinates):
            raise ValueError(f"Coordinates {coordinates} are out of bounds for grid size {self.size}.")
        return self.cells[coordinates]

    def is_valid_coordinates(self, coordinates: Coordinates) -> bool:
        """
        Check if the given coordinates are within the grid boundaries.

        Args:
            coordinates (Coordinates): The coordinates to check.

        Returns:
            bool: True if coordinates are valid, False otherwise.
        """
        return (
            0 <= coordinates.x < self.size and
            0 <= coordinates.y < self.size
        )

    def spawn_resource(self, coordinates: Coordinates, resource: Resource) -> None:
        """
        Place a resource on the cell at the given coordinates.

        Args:
            coordinates (Coordinates): The coordinates where the resource will be placed.
            resource (Resource): The resource to place.

        Raises:
            ValueError: If the coordinates are out of bounds.
        """
        if not self.is_valid_coordinates(coordinates):
            raise ValueError(f"Coordinates {coordinates} are out of bounds for grid size {self.size}.")
        cell = self.cells[coordinates]
        new_cell = Cell(coordinates=cell.coordinates, resource=resource)
        self.cells[coordinates] = new_cell

    def collect_resource_at(self, coordinates: Coordinates) -> Optional[Resource]:
        """
        Collect and remove the resource from the cell at the given coordinates.

        Args:
            coordinates (Coordinates): The coordinates to collect from.

        Returns:
            Optional[Resource]: The collected resource, or None if no resource was present.

        Raises:
            ValueError: If the coordinates are out of bounds.
        """
        if not self.is_valid_coordinates(coordinates):
            raise ValueError(f"Coordinates {coordinates} are out of bounds for grid size {self.size}.")
        cell = self.cells[coordinates]
        if cell.resource is not None:
            collected = cell.resource
            new_cell = Cell(coordinates=cell.coordinates, resource=None)
            self.cells[coordinates] = new_cell
            return collected
        return None
