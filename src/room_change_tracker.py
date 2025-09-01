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


class RoomChangeTracker:
    def __init__(self, notify: RoomChangeInterface, log: Log, debug: bool = False):
        self._notify = notify
        self._log = log
        self._debug = debug

        self._last_room = None

    def check_for_movement(self, current_room: str, command: str) -> None:
        has_moved = self._last_room is not None and self._last_room != current_room
        if has_moved:
            self._log.room(current_room)

            if self._debug:
                with open("commands.txt", "a", encoding="utf-8") as f:
                    f.write(command + "\n")

            direction = self._unify_direction(command)
            action = ExplorationAction(self._last_room, direction, current_room)
            self._notify.record_movement(action)
            self._notify.display()

        self._last_room = current_room

    def _unify_direction(self, command: str) -> str:
        match = re.match(DIRECTION_RE, command, re.IGNORECASE)
        if match:
            direction = match.group(1)
        else:
            direction = command
            # special cases: "enter window", "climb tree"
            print(f"WARN: unrecognized direction: {direction}")

        return direction.lower()
