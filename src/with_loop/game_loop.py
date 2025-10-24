from frotz.game import Game
from tools.room_change.room_change_tracker import RoomChangeTracker
from util.log import Log
from util.wait_threshold import WaitThreshold
from with_loop.loop_ai import LoopAi


class GameLoop:
    """Driver class to combine Game output with AI and vice versa."""

    def __init__(self, log: Log, ai: LoopAi, tracker: RoomChangeTracker):
        self.log = log
        self.ai = ai
        self.tracker = tracker
        self.game = None

    def start(self) -> None:
        self.game = Game()

        game_notes = self.game.get_game_play_notes()
        game_intro = self.game.get_intro()

        self.ai.start(game_notes, game_intro)

    def run(self, max_loops: int = 1000, threshold: float = 0) -> None:
        """Run the game loop with a given AI."""

        wait_threshold = WaitThreshold(threshold)
        command = "look"
        loop_count = 0
        while True:
            game_output = self.game.do_command(command)
            self.log.game(game_output)

            self.tracker.check_for_movement(self.game.room_name(), command)

            # wait for threshold
            wait_threshold.wait()

            if self.game.game_ended():
                break
            if loop_count >= max_loops:
                break

            # Get AI's next move
            command = self.ai.get_next_command(game_output)
            self.log.command(command)

            loop_count += 1

    def close(self) -> None:
        self.ai.close()
        self.game.close()
