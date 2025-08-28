from abc import ABC, abstractmethod
from map.exploration_action import ExplorationAction


class RoomChangeInterface(ABC):

    @abstractmethod
    def record_movement(self, action: ExplorationAction) -> None:
        """Process a recorded movement."""

    @abstractmethod
    def display(self) -> None:
        """Display the results of tracking."""
