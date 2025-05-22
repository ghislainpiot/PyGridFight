"""Avatar domain model for PyGridFight."""

from dataclasses import dataclass
from typing import Dict, List

from pygridfight.domain.enums import AvatarType


@dataclass
class Position:
    """Position coordinates."""
    x: int
    y: int

    def distance_to(self, other: "Position") -> int:
        """Calculate Manhattan distance to another position."""
        return abs(self.x - other.x) + abs(self.y - other.y)


@dataclass
class Avatar:
    """Avatar domain model."""

    id: str
    player_id: str
    avatar_type: AvatarType
    position: Position
    health: int = 100
    max_health: int = 100
    energy: int = 100
    max_energy: int = 100
    inventory: Dict[str, int] = None

    def __post_init__(self) -> None:
        """Initialize default values."""
        if self.inventory is None:
            self.inventory = {}

    def move_to(self, new_position: Position) -> None:
        """Move avatar to new position."""
        self.position = new_position

    def take_damage(self, damage: int) -> None:
        """Apply damage to avatar."""
        self.health = max(0, self.health - damage)

    def heal(self, amount: int) -> None:
        """Heal avatar."""
        self.health = min(self.max_health, self.health + amount)

    def use_energy(self, amount: int) -> bool:
        """Use energy if available."""
        if self.energy >= amount:
            self.energy -= amount
            return True
        return False

    def restore_energy(self, amount: int) -> None:
        """Restore energy."""
        self.energy = min(self.max_energy, self.energy + amount)

    @property
    def is_alive(self) -> bool:
        """Check if avatar is alive."""
        return self.health > 0

    @property
    def health_percentage(self) -> float:
        """Get health as percentage."""
        return (self.health / self.max_health) * 100

    @property
    def energy_percentage(self) -> float:
        """Get energy as percentage."""
        return (self.energy / self.max_energy) * 100