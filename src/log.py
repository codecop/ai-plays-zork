from pathlib import Path
from datetime import datetime


class Log:
    def __init__(self, path: str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._write_start_time()

    def _write_start_time(self) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(f"[START] {timestamp}\n")

    def _write(self, prefix: str, message: str) -> None:
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(f"{prefix} {message}\n")

    def gameText(self, text: str) -> None:
        self._write("GAME", text)

    def command(self, command: str) -> None:
        self._write("CMD", command)
