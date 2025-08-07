from typing import Dict, Optional, List
from dataclasses import dataclass, field
from .room import Room


@dataclass
class GameMap:
    rooms: Dict[str, Room] = field(default_factory=dict)
    current_room_name: Optional[str] = None
    room_history: List[str] = field(default_factory=list)

    def add_room(self, room: Room) -> None:
        self.rooms[room.name] = room

    def update_room(self, room: Room) -> None:
        self.rooms[room.name] = room

    def get_room(self, room_name: str) -> Optional[Room]:
        return self.rooms.get(room_name)

    def set_current_room(self, room_name: str) -> None:
        if self.current_room_name != room_name:
            self.current_room_name = room_name
            if not self.room_history or self.room_history[-1] != room_name:
                self.room_history.append(room_name)

    def get_current_room(self) -> Optional[Room]:
        if self.current_room_name:
            return self.get_room(self.current_room_name)
        return None

    def has_room(self, room_name: str) -> bool:
        return room_name in self.rooms

    def get_all_room_names(self) -> List[str]:
        return list(self.rooms.keys())

    def get_visited_rooms(self, max_count: int) -> List[str]:
        return self.room_history[-max_count:] if max_count > 0 else []
