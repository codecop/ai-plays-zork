from room_change_interface import RoomChangeInterface
from map.exploration_action import ExplorationAction


class NullRoomChange(RoomChangeInterface):
    def record_movement(self, action: ExplorationAction) -> None:
        pass

    def display(self) -> None:
        pass
