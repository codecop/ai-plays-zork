"""Create the dependency tree of the whole application."""

from pathlib import Path
from tools.room_change.create_tracker import create_tracker
from util.log import Log
from util.create_run import create_run
from with_loop.loop_ai import LoopAi
from with_loop.game_loop import GameLoop

from ai.claudecode.claude_code_loop_ai import ClaudeCodeLoopAi
from ai.mistralai.mistral_loop_ai import MistralLoopAi
from ai.openai.openai_loop_ai import OpenaiLoopAi


def _create_ai(config: str, run_folder: Path, log: Log) -> LoopAi:
    """Create the AI for the config."""

    ai: LoopAi
    if config.startswith("mistral"):
        ai = MistralLoopAi(config, run_folder, log)

    elif config.startswith("claudecode"):
        ai = ClaudeCodeLoopAi(config, run_folder, log)

    elif config.startswith("openai"):
        ai = OpenaiLoopAi(config, run_folder, log)

    else:
        raise ValueError(f"Invalid config: {config}")

    return ai


def create(config: str) -> GameLoop:
    run_folder, log = create_run(config, "loop")
    ai = _create_ai(config, run_folder, log)
    tracker = create_tracker(run_folder, log)

    return GameLoop(log, ai, tracker)
