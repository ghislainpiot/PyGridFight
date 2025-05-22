"""Resource domain model for PyGridFight."""

from dataclasses import dataclass
from typing import Optional

from pygridfight.domain.enums import ResourceType
from pygridfight.domain.models.avatar import Position


@dataclass
class Resource:
    """Resource domain model."""

    id: str
    resource_type: ResourceType
    position: Position
    amount: int
    max_amount: int
    respawn_time: Optional[int] = None  # seconds until respawn
    is_depleted: bool = False

    def collect(self, amount: int) -> int:
        """Collect resources and return actual amount collected."""
        if self.is_depleted:
            return 0

        actual_amount = min(amount, self.amount)
        self.amount -= actual_amount

        if self.amount <= 0:
            self.is_depleted = True

        return actual_amount

    def respawn(self) -> None:
        """Respawn the resource."""
        self.amount = self.max_amount
        self.is_depleted = False

    @property
    def collection_percentage(self) -> float:
        """Get remaining resource as percentage."""
        return (self.amount / self.max_amount) * 100 if self.max_amount > 0 else 0.0