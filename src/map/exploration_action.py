from dataclasses import dataclass
from .exit import Direction


@dataclass(frozen=True)
class ExplorationAction:
    from_room_name: str
    direction: Direction
    to_room_name: str
