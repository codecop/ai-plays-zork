from ai_interface import AiInterface
from game import Game


def run(ai: AiInterface) -> None:
    """Run the game loop with a given AI."""

    # start game
    game = Game()
    game_notes = game.get_game_play_notes()
    game_intro = game.get_intro()

    ai.start(game_notes, game_intro)

    # run loop
    command = "look"
    while True:
        game_output = game.do_command(command)
        ai.log.game(game_output)

        # Get AI's next move
        context = game_output
        command = ai.get_next_command(context)
        ai.log.command(command)

        if game.game_ended():
            break

    # close all
    ai.close()
    game.close()
