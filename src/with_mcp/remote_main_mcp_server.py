import sys
from typing import Any
from fastmcp import Context, FastMCP
from frotz.game import Game
from util.create_run import create_run
from tools.room_change.create_tracker import create_tracker


class RemoteMainMcpServer:
    """Remote MCP server around Zork game with logging like main loop."""

    def __init__(self):
        self._game: Any = None  # : Game | None
        self._log: Any = None  # : Log | None
        self._tracker: Any = None  # : RoomChangeTracker | None

        self.client = "not_initialized"

        self._mcp = FastMCP(name="remote-main-mcp-server")
        self._register_tools()

    def _register_tools(self):
        @self._mcp.tool
        def send_command(command: str, ctx: Context) -> str:
            """Send a command to the game and get the response"""
            return self._send_command(command, ctx)

        @self._mcp.tool
        def get_last_answer(ctx: Context) -> str:
            """Get the last answer from the game again"""
            return self._get_last_answer(ctx)

        @self._mcp.tool
        def get_game_status(ctx: Context) -> str:
            """Get game status (room name, number of moves, score)"""
            return self._get_game_status(ctx)

        @self._mcp.tool
        def get_gameplay_notes(ctx: Context) -> str:
            """Get the gameplay notes"""
            return self._get_gameplay_notes(ctx)

    def _initialize_game(self, client_name: str = "Unknown") -> str:
        self.client = client_name
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

    def _send_command(self, command: str, ctx: Context) -> str:
        """Send a command to the game and get the response"""

        if self._game is None:
            self._initialize_game(ctx.client_id)

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

    def _get_last_answer(self, ctx: Context) -> str:
        """Get the last answer from the game again"""

        if self._game is None:
            self._initialize_game(ctx.client_id)

        return self._last_answer

    def _get_game_status(self, ctx: Context) -> str:
        """Get game status (room name, number of moves, score)"""

        if self._game is None:
            self._initialize_game(ctx.client_id)

        return (
            f"Room: {self._game.room_name()}\n"
            f"Moves: {self._game.moves()}\n"
            f"Score: {self._game.score()}"
        )

    def _get_gameplay_notes(self, ctx: Context) -> str:
        """Get the gameplay notes"""

        if self._game is None:
            self._initialize_game(ctx.client_id)

        return self._game.get_game_play_notes()

    def run(self, host: str, port: int, debug: bool):
        self._mcp.run(transport="http", host=host, port=port, debug=debug)

    def close(self):
        self._game.close()
        self._mcp.close()


def main() -> None:
    debug_enabled = len(sys.argv) > 1 and sys.argv[1] == "--debug"
    server = RemoteMainMcpServer()
    try:
        server.run(host="127.0.0.1", port=8001, debug=debug_enabled)
    except Exception as e:
        server.close()


if __name__ == "__main__":
    main()
