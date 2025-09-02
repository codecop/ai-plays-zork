import time
from pathlib import Path
from ai import Ai
from game import Game
from log import Log
from room_change_tracker import RoomChangeTracker


class GameLoop:
    def __init__(
        self,
        run_folder: Path,
        log: Log,
        ai: Ai,
        tracker: RoomChangeTracker,
        threshold: float = 0,
    ):
        self.run_folder = run_folder
        self.log = log
        self.ai = ai
        self.tracker = tracker
        self.game = None

        self.threshold = threshold

    def start_game(self) -> None:
        self.game = Game()

        game_notes = self.game.get_game_play_notes()
        game_intro = self.game.get_intro()

        self.ai.start(game_notes, game_intro)

    def run_loop(self) -> None:
        """Run the game loop with a given AI."""

        start_time = time.time()
        command = "look"
        while True:
            game_output = self.game.do_command(command)
            self.log.game(game_output)

            self.tracker.check_for_movement(self.game.room_name(), command)

            # wait for threshold
            elapsed_time = time.time() - start_time
            if elapsed_time < self.threshold:
                time.sleep(self.threshold - elapsed_time)

            start_time = time.time()

            # Get AI's next move
            command = self.ai.get_next_command(game_output)
            self.log.command(command)

            if self.game.game_ended():
                break

    def close(self) -> None:
        self.ai.close()
        self.game.close()
