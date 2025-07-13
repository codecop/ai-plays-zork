from file_utils import getNextFolderName
from log import Log
from game import Game
from mistral_ai import MistralAi

# create run
config = "mistralai"
baseName = f"{config}-run"
runFolder = getNextFolderName(".", baseName)
log = Log(runFolder)

# start game
game = Game()
game_notes = game.get_game_play_notes()
game_intro = game.get_intro()

# init AI
ai = MistralAi(config, runFolder, log)
ai.start(game_notes, game_intro)

# run loop
command = "look"
while True:
    game_output = game.do_command(command)
    log.game(game_output)

    # Get AI's next move
    context = f"Game answers with {game_output}"
    command = ai.get_next_command(context)
    log.command(command)

    if game.game_ended():
        break

ai.close()
game.close()
# maybe save statistics
