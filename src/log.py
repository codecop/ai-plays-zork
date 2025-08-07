from pathlib import Path
from datetime import datetime
from file_utils import ENCODING


class AnsiColors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    RESET = "\033[0m"


class Log:
    """Record the output of the game and the AI to console and a log file."""

    def __init__(self, path: Path):
        self.path = path / "log.txt"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._write_start_time()

    def _write_start_time(self) -> None:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._write("START", now, AnsiColors.CYAN)

    def ai(self, text: str) -> None:
        self._write("AI   ", text, AnsiColors.YELLOW)

    def game(self, text: str) -> None:
        self._write("GAME ", text, AnsiColors.RED)

    def command(self, command: str) -> None:
        self._write("CMD  ", command, AnsiColors.GREEN)

    def _write(self, prefix: str, message: str, color: str = "") -> None:
        lines = message.split("\n")

        log_message = f"{prefix} {lines[0]}"
        spacer = " " * (len(prefix) + 1)
        for line in lines[1:]:
            log_message += f"\n{spacer}{line}"

        self._log(log_message)
        print(f"{color}{log_message}{AnsiColors.RESET}", flush=True)

    def _log(self, message: str) -> None:
        with open(self.path, "a", encoding=ENCODING) as f:
            f.write(f"{message}\n")
