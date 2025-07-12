from pathlib import Path
from datetime import datetime


# ANSI color codes
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    RESET = "\033[0m"


class Log:
    def __init__(self, path: str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._write_start_time()

    def _write_start_time(self) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._write("START", timestamp, Colors.CYAN)

    def room(self, text: str) -> None:
        self._write("ROOM", text, Colors.RED)

    def gameText(self, text: str) -> None:
        self._write("GAME", text, Colors.GREEN)

    def command(self, command: str) -> None:
        self._write("CMD", command, Colors.YELLOW)

    def _write(self, prefix: str, message: str, color: str = "") -> None:
        log_message = f"{prefix} {message}"
        self._log(log_message)
        print(f"{color}{log_message}{Colors.RESET}")

    def _log(self, message: str) -> None:
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(f"{message}\n")
