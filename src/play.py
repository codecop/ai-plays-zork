from file_utils import getNextFolderName, readGamePlayNotes
from log import Log
from pyfrotz import Frotz
from mistral_ai import MistralAi

ai = MistralAi()

# create run
baseName = f"{ai.name()}-run"
folderName = getNextFolderName(".", baseName)
log = Log(folderName)

# start game
game = Frotz("data/zork1.z3")
game_intro = game.get_intro()
game_notes = readGamePlayNotes()

# init AI
ai.init(game_notes, game_intro)

# run loop
command = "look"
while True:
    room, description = game.do_command(command)
    # TODO remove whitespace etc.
    log.room(room)
    log.gameText(description)

    # scan answer for "you are dead"

    # Get AI's next move
    context = f"You are in {room}.\n{description}"
    command = ai.get_next_command(context)
    log.command(command)

    if game.game_ended():
        break

# game.do_command("quit")
# game.do_command("y")

ai.close()

# close game resources
game.frotz.stdin.close()
game.frotz.stdout.close()
game.frotz.wait()

# maybe save statistics
