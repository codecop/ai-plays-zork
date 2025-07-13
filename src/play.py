from file_utils import getNextFolderName, readGamePlayNotes
from log import Log
from pyfrotz import Frotz
from mistral_ai import MistralAi

# create run
config = "mistralai"
baseName = f"{config}-run"
runFolder = getNextFolderName(".", baseName)
log = Log(runFolder)

# start game
game = Frotz("data/zork1.z3")
game_intro = game.get_intro()
game_notes = readGamePlayNotes()

# init AI
config = MistralAi(config, runFolder, log)
config.start(game_notes, game_intro)

# run loop
command = "look"
while True:
    room, description = game.do_command(command)
    # TODO remove whitespace etc.
    log.game(f"{room}\n{description}")

    # scan answer for "you are dead"

    # Get AI's next move
    context = f"Game answers with {room}\n{description}"
    command = config.get_next_command(context)
    log.command(command)

    if game.game_ended():
        break

# game.do_command("quit")
# game.do_command("y")

config.close()

# close game resources
game.frotz.stdin.close()
game.frotz.stdout.close()
game.frotz.wait()

# maybe save statistics
