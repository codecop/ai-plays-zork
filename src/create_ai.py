from ai_interface import AiInterface
from claude_code_ai import ClaudeCodeAi
from file_utils import next_folder_name
from log import Log
from mistral_ai import MistralAi


def create_ai(config: str) -> AiInterface:
    """Create a given AI for the config."""

    # create run
    base_name = f"{config}-run"
    run_folder = next_folder_name(".", base_name)
    log = Log(run_folder)

    # create AI
    if config.startswith("mistral"):
        ai = MistralAi(config, run_folder, log)

    elif config.startswith("claudecode"):
        ai = ClaudeCodeAi(config, run_folder, log)

    else:
        raise ValueError(f"Invalid config: {config}")

    return ai
