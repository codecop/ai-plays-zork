from pyfrotz import Frotz
from file_utils import readFile


class Game:
    def __init__(self, game_file: str = "data/zork1.z3"):
        self.wrapper = Frotz(game_file)

    def get_game_play_notes(self) -> str:
        return readFile("data/Zork Gameplay Notes.txt")

    def get_intro(self) -> str:
        return self.wrapper.get_intro()

    def do_command(self, command: str) -> str:
        room, description = self.wrapper.do_command(command)
        # TODO remove whitespace etc.
        return f"{room}\n{description}"

    def game_ended(self) -> bool:
        return self.wrapper.game_ended()

    def close(self) -> None:
        # self.do_command("quit")
        # self.do_command("y")

        if self.wrapper:
            self.wrapper.frotz.stdin.close()
            self.wrapper.frotz.stdout.close()
            self.wrapper.frotz.wait()
            self.wrapper = None
