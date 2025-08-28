import re
from log import Log
from room_change_interface import RoomChangeInterface
from map.exploration_action import ExplorationAction

# order is relevant for regex matching
DIRECTIONS = [
    "north",
    "east",
    "south",
    "west",
    "northeast",
    "southeast",
    "southwest",
    "northwest",
    "up",
    "down",
]
DIRECTION_RE = ".*(" + "|".join(DIRECTIONS) + ").*"


class RoomName:
    def __init__(self, tracker: RoomChangeInterface, log: Log, debug: bool = False):
        self.tracker = tracker
        self.log = log
        self.debug = debug

        self.last_room = None

    def check_for_movement(self, current_room: str, command: str) -> None:
        has_moved = self.last_room is not None and self.last_room != current_room
        if has_moved:
            self.log.room(current_room)

            if self.debug:
                with open("commands.txt", "a", encoding="utf-8") as f:
                    f.write(command + "\n")

            direction = self._unify_direction(command)
            action = ExplorationAction(self.last_room, direction, current_room)
            self.tracker.record_movement(action)

        self.last_room = current_room

    def _unify_direction(self, command: str) -> str:
        match = re.match(DIRECTION_RE, command, re.IGNORECASE)
        if match:
            direction = match.group(1)
        else:
            direction = command
            # special cases: "enter window", "climb tree"
            print(f"WARN: unrecognized direction: {direction}")

        return direction.lower()
