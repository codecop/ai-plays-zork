from pathlib import Path
from datetime import datetime


class AnsiColors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    RESET = "\033[0m"


class Log:
    def __init__(self, path: str):
        self.path = Path(path + "/log.txt")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._write_start_time()

    def _write_start_time(self) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._write("START", timestamp, AnsiColors.CYAN)

    def room(self, text: str) -> None:
        self._write("ROOM", text, AnsiColors.RED)

    def gameText(self, text: str) -> None:
        self._write("GAME", text, AnsiColors.GREEN)

    def command(self, command: str) -> None:
        self._write("CMD", command, AnsiColors.YELLOW)

    def _write(self, prefix: str, message: str, color: str = "") -> None:
        log_message = f"{prefix} {message}"
        self._log(log_message)
        print(f"{color}{log_message}{AnsiColors.RESET}")

    def _log(self, message: str) -> None:
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(f"{message}\n")
