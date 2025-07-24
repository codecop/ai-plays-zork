import sys
from game import Game
from create_ai import create_ai


# init AI
if len(sys.argv) > 1:
    config = sys.argv[1]
else:
    raise ValueError("No config provided")

ai = create_ai(config)

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

ai.close()
game.close()
