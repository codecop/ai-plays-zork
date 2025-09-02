from pathlib import Path
from file_utils import ENCODING
from log import Log


class CommandLog(Log):
    """Record the ai commands to log files."""

    def __init__(self, path: Path, name: str):
        super().__init__()
        self.room_path = path / f"{name}rooms.txt"
        self.room_path.parent.mkdir(parents=True, exist_ok=True)
        self.command_path = path / f"{name}commands.txt"
        self.command_path.parent.mkdir(parents=True, exist_ok=True)

    def ai(self, text: str) -> None:
        pass

    def game(self, text: str) -> None:
        pass

    def command(self, command: str) -> None:
        self._log_separate(self.command_path, command)

    def room(self, text: str) -> None:
        self._log_separate(self.room_path, text)

    def _log_separate(self, path: Path, message: str) -> None:
        with open(path, "a", encoding=ENCODING) as f:
            f.write(f"{message}\n")
