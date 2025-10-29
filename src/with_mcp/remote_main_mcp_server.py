import os
import sys
from typing import Any
from fastmcp import Context, FastMCP


working_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, working_dir)


from frotz.game import Game
from util.create_run import create_run
from tools.room_change.create_tracker import create_tracker


class RemoteMainMcpServer:
    """Remote MCP server around Zork game with logging like main loop."""

    def __init__(self):
        self._game = Game()
        self._log: Any = None  # : Log | None
        self._tracker: Any = None  # : RoomChangeTracker | None
        self._last_answer = ""

        self.client = "not_initialized"

        self._mcp = FastMCP(name="remote-main-mcp-server")
        self._register_tools()

    def _register_tools(self) -> None:
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

    def _initialize_game(self, client_name="Unknown") -> None:
        self.client = client_name

        config = client_name
        run_folder, self._log = create_run(config, "mcp")
        self._tracker = create_tracker(run_folder, self._log, False)
        self._log.ai(
            "ai: remote-main-mcp-server\n"
            + f"configuration: {config}\n"
            + f"name: {config}"
        )

        self._last_answer = self._game.get_intro()

    def _send_command(self, command: str, ctx: Context) -> str:
        """Send a command to the game and get the response"""

        if self._log is None:
            self._initialize_game(ctx.session._client_params.clientInfo.name)

        # Get AI's next move
        if self._log:
            self._log.command(command)

        # Send command to game
        game_output = self._game.do_command(command)
        self._last_answer = game_output

        if self._log:
            self._log.game(game_output)

        if self._tracker:
            self._tracker.check_for_movement(self._game.room_name(), command)

        return game_output

    def _get_last_answer(self, ctx: Context) -> str:
        """Get the last answer from the game again"""

        if self._log is None:
            self._initialize_game(ctx.session._client_params.clientInfo.name)

        return self._last_answer

    def _get_game_status(self, ctx: Context) -> str:
        """Get game status (room name, number of moves, score)"""

        if self._log is None:
            self._initialize_game(ctx.session._client_params.clientInfo.name)

        return (
            f"Room: {self._game.room_name()}\n"
            f"Moves: {self._game.moves()}\n"
            f"Score: {self._game.score()}"
        )

    def _get_gameplay_notes(self, ctx: Context) -> str:
        """Get the gameplay notes"""

        if self._log is None:
            self._initialize_game(ctx.session._client_params.clientInfo.name)

        return self._game.get_game_play_notes()

    def run(self, host: str, port: int) -> None:
        self._mcp.run(transport="http", host=host, port=port)

    def close(self) -> None:
        self._game.close()


def main() -> None:
    server = RemoteMainMcpServer()
    try:
        server.run(host="127.0.0.1", port=8001)
    except Exception as e:
        server.close()
        raise e


if __name__ == "__main__":
    main()
