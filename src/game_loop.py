from ai import Ai
from frotz.game import Game
from tools.room_change.room_change_tracker import RoomChangeTracker
from util.log import Log
from util.wait_threshold import WaitThreshold


class GameLoop:
    """Driver class to combine Game output with AI and vice versa."""

    def __init__(self, log: Log, ai: Ai, tracker: RoomChangeTracker):
        self.log = log
        self.ai = ai
        self.tracker = tracker
        self.game = None

    def start(self) -> None:
        self.game = Game()

        game_notes = self.game.get_game_play_notes()
        game_intro = self.game.get_intro()

        self.ai.start(game_notes, game_intro)

    def run(self, threshold: float = 0) -> None:
        """Run the game loop with a given AI."""

        wait_threshold = WaitThreshold(threshold)
        command = "look"
        while True:
            game_output = self.game.do_command(command)
            self.log.game(game_output)

            self.tracker.check_for_movement(self.game.room_name(), command)

            # wait for threshold
            wait_threshold.wait()

            # Get AI's next move
            command = self.ai.get_next_command(game_output)
            self.log.command(command)

            if self.game.game_ended():
                break

    def close(self) -> None:
        self.ai.close()
        self.game.close()
