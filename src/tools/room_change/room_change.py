from abc import ABC, abstractmethod
from tools.room_change.exploration_action import ExplorationAction


class RoomChange(ABC):
    """Base class for tracking of room changes."""

    @abstractmethod
    def record_movement(self, action: ExplorationAction) -> None:
        """Process a room change movement."""

    @abstractmethod
    def display(self) -> None:
        """Display the results of tracking."""
