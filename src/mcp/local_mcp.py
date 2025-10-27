import sys
import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class LocalMcp(ABC):
    """Base class for local (i.e. stdio) MCP servers."""

    def __init__(self, debug: bool = False):
        self._is_debug = debug
        self._debug(f"Starting {self.__class__.__name__}")
        self.client = "not_initialized"

    def _debug(self, message: str) -> None:
        if not self._is_debug:
            return

        print(f"DEBUG: {message}", file=sys.stderr)
        sys.stderr.flush()

        log_file = Path(__file__).with_suffix(".log")
        with log_file.open("a", encoding="utf-8") as fp:
            fp.write(f"DEBUG: {message}\n")

    def run(self) -> None:
        while self._run_single():
            pass

    def _run_single(self) -> bool:
        try:
            message = self._read_message()
            if message is None:
                return False

            method = message.get("method")
            request_id = message.get("id")
            params = message.get("params", {})

            if method == "initialize":
                response = self.handle_initialize(request_id, params)
            elif method == "tools/list":
                response = self.handle_tools_list(request_id)
            elif method == "tools/call":
                response = self.handle_tools_call(request_id, params)
            else:
                response = self._handle_not_found(request_id, method)

            self._write_message(response)

        except Exception as e:
            self._debug(f"Error in {method}: {repr(e)}")
            # continue the loop

        return True

    def _read_message(self):  # -> dict[str, Any] | None:
        line = sys.stdin.readline()
        if not line:
            return None
        self._debug("---")
        self._debug(f"Read line: {line.strip()}")
        return json.loads(line.strip())

    def handle_initialize(self, request_id, params: dict):
        self._debug(f"Handling initialize request: {request_id}")
        self.client = params.get("clientInfo", {}).get("name", "unknown-client")
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": self.name(), "version": "1.0.0"},
            },
        }

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def handle_tools_list(self, request_id):
        pass

    @abstractmethod
    def handle_tools_call(self, request_id, params: dict):
        pass

    def _handle_text_result(self, request_id, text: str):
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": [{"type": "text", "text": text}]},
        }

    def _handle_not_found(self, request_id, method):
        return self._handle_error(request_id, -32601, f"Method not found: {method}")

    def _handle_error(self, request_id, code: int, message: str):
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message,
            },
        }

    def _write_message(self, message: dict):
        sys.stdout.write(json.dumps(message) + "\n")
        sys.stdout.flush()
        self._debug(f"Wrote message: {message}")

    def close(self) -> None:
        self._debug(f"Stopping {self.__class__.__name__}")
