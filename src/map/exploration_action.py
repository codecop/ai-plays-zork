from dataclasses import dataclass


@dataclass(frozen=True)
class ExplorationAction:
    from_room_name: str
    direction: str
    to_room_name: str
