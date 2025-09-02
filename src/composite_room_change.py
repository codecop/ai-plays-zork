from room_change_interface import RoomChangeInterface
from map.exploration_action import ExplorationAction


class CompositeRoomChange(RoomChangeInterface):
    def __init__(self, *changes: RoomChangeInterface) -> None:
        self.changes = changes

    def record_movement(self, action: ExplorationAction) -> None:
        for change in self.changes:
            change.record_movement(action)

    def display(self) -> None:
        for change in self.changes:
            change.display()
