import sys
from typing import Any
from fastmcp import FastMCP
from frotz.game import Game
from util.create_run import create_run
from tools.room_change.create_tracker import create_tracker


class RemoteMainMcpServer:
    """Remote MCP server around Zork game with logging like main loop."""

    def __init__(self):
        self._game: Any = None  # : Game | None
        self._log: Any = None  # : Log | None
        self._tracker: Any = None  # : RoomChangeTracker | None

        self._client_info: dict = {}

        self._mcp = FastMCP(name="remote-main-mcp-server")
        self._register_tools()

    def _register_tools(self):
        @self._mcp.tool
        def send_command(command: str) -> str:
            """Send a command to the game and get the response"""
            return self._send_command(command)

    def _initialize_game(self, client_name: str) -> str:
        self._client_info = {"name": client_name}
        self._game = Game()

        config = client_name
        run_folder, self._log = create_run(config, "mcp")
        self._tracker = create_tracker(run_folder, self._log, False)
        self._log.ai(
            f"ai: remote-main-mcp-server\n"
            + f"configuration: {config}\n"
            + f"name: {config}"
        )

        return self._game.start()

    def _send_command(self, command: str) -> str:
        # Get AI's next move
        if self._log:
            self._log.command(command)

        # Send command to game
        game_output = self._game.send_command(command)

        if self._log:
            self._log.game(game_output)

        if self._tracker:
            self._tracker.check_for_movement(self._game.room_name(), command)

        return game_output

    def run(self, host: str, port: int, debug: bool):
        self._mcp.run(transport="http", host=host, port=port, debug=debug)


def main() -> None:
    debug_enabled = len(sys.argv) > 1 and sys.argv[1] == "--debug"
    server = RemoteMainMcpServer()
    server.run(host="127.0.0.1", port=8001, debug=debug_enabled)


if __name__ == "__main__":
    main()
