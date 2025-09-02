from pathlib import Path
from file_utils import ENCODING
from log import Log


class IndividualLog(Log):
    """Record the ai commands and rooms to individual log files each."""

    def __init__(self, path: Path, name: str):
        super().__init__()
        path.mkdir(parents=True, exist_ok=True)

        self.room_path = path / f"{name}rooms.txt"
        self.command_path = path / f"{name}commands.txt"
        self.warn_path = path / f"{name}warnings.txt"

    def ai(self, text: str) -> None:
        pass

    def game(self, text: str) -> None:
        pass

    def command(self, command: str) -> None:
        self._log_separate(self.command_path, command)

    def room(self, text: str) -> None:
        self._log_separate(self.room_path, text)

    def warn(self, text: str) -> None:
        self._log_separate(self.warn_path, text)

    def _log_separate(self, path: Path, message: str) -> None:
        with open(path, "a", encoding=ENCODING) as f:
            f.write(f"{message}\n")
