from pathlib import Path
from file_utils import ENCODING


class CommandLog:
    """Record the ai commands to log files."""

    def __init__(self, path: Path, name: str):
        self.path = path / f"{name}_commands.txt"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def command(self, command: str) -> None:
        self._log(self.path, command)

    def _log(self, path: Path, message: str) -> None:
        with open(path, "a", encoding=ENCODING) as f:
            f.write(f"{message}\n")
