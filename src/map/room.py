from typing import Dict
from dataclasses import dataclass
from .exit import Exit


@dataclass(frozen=True)
class Room:
    name: str
    description: str
    exits: Dict[str, Exit]

    def add_exit(self, exit: Exit) -> "Room":
        new_exits = self.exits.copy()
        new_exits[exit.direction] = exit
        return Room(name=self.name, description=self.description, exits=new_exits)

    def update_exit(self, direction: str, exit: Exit) -> "Room":
        new_exits = self.exits.copy()
        new_exits[direction] = exit
        return Room(name=self.name, description=self.description, exits=new_exits)

    def get_exit(self, direction: str) -> Exit:
        return self.exits.get(direction)

    def get_available_directions(self) -> list[str]:
        return list(self.exits.keys())

    def get_unexplored_exits(self) -> list[Exit]:
        return [exit for exit in self.exits.values() if not exit.was_taken]
