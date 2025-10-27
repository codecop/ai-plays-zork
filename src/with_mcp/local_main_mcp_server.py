import sys
from typing import Any
from frotz.local_game_mcp_server import GameMcpServer, working_dir
from util.create_run import create_run
from tools.room_change.create_tracker import create_tracker

# from util.log import Log
# from tools.room_change.room_change_tracker import RoomChangeTracker


class MainMcpServer(GameMcpServer):
    """MCP server around Zork game with logging like main loop."""

    def __init__(self, debug: bool = False):
        super().__init__(debug)
        self.log: Any = None  # : Log | None
        self.tracker: Any = None  # : RoomChangeTracker | None

    def name(self) -> str:
        return "local-main-mcp-server"

    def handle_initialize(self, request_id, params: dict):
        response = super().handle_initialize(request_id, params)

        config = self.client
        run_folder, self.log = create_run(config, "mcp", working_dir())
        self.tracker = create_tracker(run_folder, self.log, False)
        self.log.ai(
            f"ai: {self.__class__}\n"  #
            + f"configuration: {config}\n"
            + f"name: {config}"
        )
        return response

    def handle_send_command(self, command: str) -> str:
        # Get AI's next move
        if self.log:
            self.log.command(command)

        # Send command to game
        game_output = super().handle_send_command(command)
        if self.log:
            self.log.game(game_output)

        if self.tracker:
            self.tracker.check_for_movement(self._game.room_name(), command)

        return game_output


def main() -> None:
    debug_enabled = len(sys.argv) > 1 and sys.argv[1] == "--debug"
    server = MainMcpServer(debug_enabled)
    server.run()
    server.close()


if __name__ == "__main__":
    main()
