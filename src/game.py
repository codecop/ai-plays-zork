from pyfrotz import Frotz
from file_utils import readFile
import re


class Game:
    def __init__(self, game_file: str = "data/zork1.z3"):
        self.wrapper = Frotz(game_file)
        self.has_quit = False

    def get_game_play_notes(self) -> str:
        return readFile("data/Zork Gameplay Notes.txt")

    def get_intro(self) -> str:
        return self.wrapper.get_intro()

    def do_command(self, command: str) -> str:
        answer = self.wrapper.do_command(command)
        room, description = answer
        first = self.strip_whitespaces(room)
        second = self.strip_whitespaces(description)
        if second:
            return f"{first}\n{second}"
        return first

    def strip_whitespaces(self, text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

    def game_ended(self) -> bool:
        return self.wrapper.game_ended()

    def quit(self) -> None:
        self.has_quit = True
        self.wrapper.do_command("quit")
        self.wrapper.do_command("y")

    def close(self) -> None:
        if not self.has_quit:
            self.quit()

        if self.wrapper:
            self.wrapper.frotz.stdin.close()
            self.wrapper.frotz.stdout.close()
            self.wrapper.frotz.wait()
            self.wrapper = None
