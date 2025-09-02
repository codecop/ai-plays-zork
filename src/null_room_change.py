from room_change import RoomChange
from map.exploration_action import ExplorationAction


class NullRoomChange(RoomChange):
    def record_movement(self, action: ExplorationAction) -> None:
        pass

    def display(self) -> None:
        pass
