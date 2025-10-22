from tools.room_change.exploration_action import ExplorationAction
from tools.room_change.room_change import RoomChange


class CompositeRoomChange(RoomChange):
    """Room Change combining multiple change as one."""

    def __init__(self, *changes: RoomChange) -> None:
        self.changes = changes

    def record_movement(self, action: ExplorationAction) -> None:
        for change in self.changes:
            change.record_movement(action)

    def display(self) -> None:
        for change in self.changes:
            change.display()
