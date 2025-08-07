from typing import Dict
from dataclasses import dataclass
from .exit import Exit, Direction


@dataclass(frozen=True)
class Room:
    name: str
    description: str
    exits: Dict[Direction, Exit]

    def add_exit(self, new_exit: Exit) -> "Room":
        new_exits = self.exits.copy()
        new_exits[new_exit.direction] = new_exit
        return Room(name=self.name, description=self.description, exits=new_exits)

    def update_exit(self, direction: Direction, new_exit: Exit) -> "Room":
        new_exits = self.exits.copy()
        new_exits[direction] = new_exit
        return Room(name=self.name, description=self.description, exits=new_exits)

    def get_exit(self, direction: Direction) -> Exit:
        return self.exits.get(direction)

    def get_available_directions(self) -> list[Direction]:
        return list(self.exits.keys())

    def get_unexplored_exits(self) -> list[Exit]:
        return [exit for exit in self.exits.values() if not exit.was_taken]
