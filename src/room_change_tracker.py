import re
from log import Log
from room_change import RoomChange
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
    """Keep track of current room and when a room has changed."""

    def __init__(self, notify: RoomChange, log: Log, move_log: Log):
        self._notify = notify
        self._log = log
        self._move_log = move_log

        self._last_room = None

    def check_for_movement(self, current_room: str, command: str) -> bool:
        has_moved = self._last_room is not None and self._last_room != current_room
        if has_moved:
            self._log.room(current_room)
            if self._move_log:
                self._move_log.command(command)

            direction = self._unify_direction(command)
            action = ExplorationAction(self._last_room, direction, current_room)
            self._notify.record_movement(action)
            self._notify.display()

        self._last_room = current_room
        return has_moved

    def _unify_direction(self, command: str) -> str:
        match = re.match(DIRECTION_RE, command, re.IGNORECASE)
        if match:
            direction = match.group(1)
        else:
            direction = command
            # special cases: "enter window", "climb tree"
            self._log.warn(f"unrecognized direction: {direction}")

        return direction.lower()
