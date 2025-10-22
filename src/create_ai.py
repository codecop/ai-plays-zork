"""Create the dependency tree of the whole application."""

from pathlib import Path
from ai import Ai
from claude_code_ai import ClaudeCodeAi
from tools.room_change.composite_room_change import CompositeRoomChange
from game_loop import GameLoop
from tools.room_change.graphviz_room_change import GraphvizRoomChange
from util.individual_log import IndividualLog
from util.file_utils import next_folder_name
from util.composite_log import CompositeLog
from util.log import Log
from util.nice_log import NiceLog
from mistral_ai import MistralAi
from tools.room_change.room_change_tracker import RoomChangeTracker


def _create_run(config: str) -> (Path, Log):
    """Create the run folder and log writing into it."""

    base_name = f"{config}-run"
    run_folder = next_folder_name(".", base_name)
    log = CompositeLog(NiceLog(run_folder), IndividualLog(run_folder, ""))

    return run_folder, log


def _create_ai(config: str, run_folder: Path, log: Log) -> Ai:
    """Create the AI for the config."""

    if config.startswith("mistral"):
        ai = MistralAi(config, run_folder, log)

    elif config.startswith("claudecode"):
        ai = ClaudeCodeAi(config, run_folder, log)

    else:
        raise ValueError(f"Invalid config: {config}")

    return ai


def _create_tracker(run_folder: Path, log: Log) -> RoomChangeTracker:
    return RoomChangeTracker(
        CompositeRoomChange(GraphvizRoomChange(run_folder)),
        log,
        IndividualLog(run_folder, "move_"),
    )


def create(config: str) -> GameLoop:
    run_folder, log = _create_run(config)
    ai = _create_ai(config, run_folder, log)
    tracker = _create_tracker(run_folder, log)

    return GameLoop(log, ai, tracker)
