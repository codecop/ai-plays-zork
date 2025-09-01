from abc import ABC, abstractmethod
from map.exploration_action import ExplorationAction


class RoomChangeInterface(ABC):

    @abstractmethod
    def record_movement(self, action: ExplorationAction) -> None:
        """Process a room change movement."""

    @abstractmethod
    def display(self) -> None:
        """Display the results of tracking."""


class NullRoomChange(RoomChangeInterface):
    def record_movement(self, action: ExplorationAction) -> None:
        pass

    def display(self) -> None:
        pass


class CompositeRoomChange(RoomChangeInterface):
    def __init__(self, *changes: RoomChangeInterface) -> None:
        self.changes = changes

    def record_movement(self, action: ExplorationAction) -> None:
        for change in self.changes:
            change.record_movement(action)

    def display(self) -> None:
        for change in self.changes:
            change.display()
