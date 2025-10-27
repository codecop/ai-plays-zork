import sys
from pathlib import Path
from frotz.game import Game
from mcp.local_mcp import LocalMcp


def working_dir() -> str:
    return str(Path(__file__).resolve().parent.parent.parent)


class GameMcpServer(LocalMcp):
    """MCP server around Zork game."""

    def __init__(self, debug: bool = False):
        super().__init__(debug)

        self._debug(f"Loading game from {working_dir()}")
        self._game = Game(working_dir=working_dir())
        self._last_answer = self._game.get_intro()

    def name(self) -> str:
        return "local-game-mcp-server"

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
                game_response = self.handle_send_command(command)
                self._debug(f'Game responds: "{game_response}"')
                self._last_answer = game_response
                return self._handle_text_result(request_id, game_response)

            if tool_name == "get_last_answer":
                return self._handle_text_result(
                    request_id, self.handle_get_last_answer()
                )

            if tool_name == "get_game_status":
                return self._handle_text_result(
                    request_id, self.handle_get_game_status()
                )

            if tool_name == "get_gameplay_notes":
                return self._handle_text_result(
                    request_id, self.handle_get_gameplay_notes()
                )

            return self._handle_error(request_id, -32601, f"Unknown tool: {tool_name}")

        except Exception as e:
            self._debug(f"Error in tools/call: {repr(e)}")
            return self._handle_error(request_id, -32603, f"Internal error: {str(e)}")

    def handle_send_command(self, command: str) -> str:
        return self._game.do_command(command)

    def handle_get_last_answer(self) -> str:
        return self._last_answer

    def handle_get_game_status(self) -> str:
        return (
            f"Room: {self._game.room_name()}\n"
            f"Moves: {self._game.moves()}\n"
            f"Score: {self._game.score()}"
        )

    def handle_get_gameplay_notes(self) -> str:
        return self._game.get_game_play_notes()

    def close(self) -> None:
        super().close()
        self._game.close()


def main() -> None:
    debug_enabled = len(sys.argv) > 1 and sys.argv[1] == "--debug"
    server = GameMcpServer(debug_enabled)
    server.run()
    server.close()


if __name__ == "__main__":
    main()
