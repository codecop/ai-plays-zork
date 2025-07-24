from ai_interface import AiInterface
from game import Game
import time


def run(ai: AiInterface, threshold: float = 0) -> None:
    """Run the game loop with a given AI."""

    # start game
    game = Game()
    game_notes = game.get_game_play_notes()
    game_intro = game.get_intro()

    ai.start(game_notes, game_intro)

    # run loop
    start_time = time.time()
    command = "look"
    while True:
        game_output = game.do_command(command)
        ai.log.game(game_output)

        # wait for threshold
        elapsed_time = time.time() - start_time
        if elapsed_time < threshold:
            time.sleep(threshold - elapsed_time)

        start_time = time.time()

        # Get AI's next move
        command = ai.get_next_command(game_output)
        ai.log.command(command)

        if game.game_ended():
            break

    # close all
    ai.close()
    game.close()
