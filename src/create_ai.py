from file_utils import getNextFolderName
from log import Log
from ai_interface import AiInterface
from claude_code_ai import ClaudeCodeAi
from mistral_ai import MistralAi


def create_ai(config: str) -> AiInterface:
    # create run
    baseName = f"{config}-run"
    runFolder = getNextFolderName(".", baseName)
    log = Log(runFolder)

    # init AI
    if config == "mistralai":
        ai = MistralAi(config, runFolder, log)

    elif config == "claudecode":
        ai = ClaudeCodeAi(config, runFolder, log)

    else:
        raise ValueError(f"Invalid config: {config}")

    return ai
