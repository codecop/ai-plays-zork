import sys
import json
from pathlib import Path
from typing import Any


def root_dir() -> Path:
    return Path(__file__).resolve().parent.parent.parent


try:
    from frotz.game import Game
except ModuleNotFoundError:
    # if started standalone need to fix the import path
    sys.path.insert(0, str(root_dir() / "src"))
    from frotz.game import Game


class GameMcpServer:
    """MCP server around Game."""

    def __init__(self, debug: bool = False):
        self._is_debug = debug
        self._debug("Starting GameMcpServer")

        base_folder = str(root_dir() / "frotz/data")
        self._game = Game(base_folder)
        self._debug(f"Loading game from {base_folder}")
        self._last_answer = self._game.get_intro()

    def _debug(self, message: str) -> None:
        if not self._is_debug:
            return

        print(f"DEBUG: {message}", file=sys.stderr)
        sys.stderr.flush()

        log_file = Path(__file__).with_suffix(".log")
        with log_file.open("a", encoding="utf-8") as fp:
            fp.write(f"DEBUG: {message}\n")

    def _read_message(self) -> dict[str, Any] | None:
        line = sys.stdin.readline()
        if not line:
            return None
        self._debug("---")
        self._debug(f"Read line: {line.strip()}")
        return json.loads(line.strip())

    def _write_message(self, message: dict):
        sys.stdout.write(json.dumps(message) + "\n")
        sys.stdout.flush()
        self._debug(f"Wrote message: {message}")

    def handle_initialize(self, request_id):
        self._debug(f"Handling initialize request: {request_id}")
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "local-game-mcp-server", "version": "1.0.0"},
            },
        }

    def handle_tools_list(self, request_id):
        self._debug(f"Handling tools/list request: {request_id}")
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": [
                    {
                        "name": "send_command",
                        "description": "Send a command to the game and get the response",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "command": {
                                    "type": "string",
                                    "description": "The command to send to the game",
                                },
                            },
                            "required": ["command"],
                        },
                    },
                    {
                        "name": "get_last_answer",
                        "description": "Get the last answer from the game again",
                        "inputSchema": {
                            "type": "object",
                            "properties": {},
                        },
                    },
                    {
                        "name": "get_game_status",
                        "description": "Get game status (room name, number of moves, score)",
                        "inputSchema": {
                            "type": "object",
                            "properties": {},
                        },
                    },
                    {
                        "name": "get_gameplay_notes",
                        "description": "Get the gameplay notes",
                        "inputSchema": {
                            "type": "object",
                            "properties": {},
                        },
                    },
                ]
            },
        }

    def handle_tools_call(self, request_id, params: dict):
        self._debug(f"Handling tools/call request: {request_id}")
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        try:
            if tool_name == "send_command":
                command = arguments.get("command", "")
                self._debug(f'Send "{command}" to game')
                result = self._game.do_command(command)
                self._debug(f'Game responds: "{result}"')
                self._last_answer = result
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"content": [{"type": "text", "text": result}]},
                }

            if tool_name == "get_last_answer":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": self._last_answer}]
                    },
                }

            if tool_name == "get_game_status":
                status_text = (
                    f"Room: {self._game.room_name()}\n"
                    f"Moves: {self._game.moves()}\n"
                    f"Score: {self._game.score()}"
                )
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"content": [{"type": "text", "text": status_text}]},
                }

            if tool_name == "get_gameplay_notes":
                notes = self._game.get_game_play_notes()
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"content": [{"type": "text", "text": notes}]},
                }

            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"},
            }

        except Exception as e:
            self._debug(f"Error in tools/call: {repr(e)}")
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"},
            }

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
                response = self.handle_initialize(request_id)
            elif method == "tools/list":
                response = self.handle_tools_list(request_id)
            elif method == "tools/call":
                response = self.handle_tools_call(request_id, params)
            else:
                response = self._handle_not_found(request_id, method)

            self._write_message(response)

        except Exception as e:
            self._debug(f"Error in run: {repr(e)}")
        return True

    def _handle_not_found(self, request_id, method):
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32601,
                "message": f"Method not found: {method}",
            },
        }

    def close(self) -> None:
        self._game.close()
        self._debug("Stopping GameMcpServer")


def main() -> None:
    debug_enabled = len(sys.argv) > 1 and sys.argv[1] == "--debug"
    server = GameMcpServer(debug_enabled)
    server.run()
    server.close()


if __name__ == "__main__":
    main()
