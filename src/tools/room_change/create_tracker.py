from pathlib import Path
from util.log import Log
from util.individual_log import IndividualLog
from tools.room_change.composite_room_change import CompositeRoomChange
from tools.room_change.graphviz_room_change import GraphvizRoomChange
from tools.room_change.room_change_tracker import RoomChangeTracker


def create_tracker(run_folder: Path, log: Log, view: bool = True) -> RoomChangeTracker:
    return RoomChangeTracker(
        CompositeRoomChange(GraphvizRoomChange(run_folder, view)),
        log,
        IndividualLog(run_folder, "move_"),
    )
