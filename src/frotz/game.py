import os.path
import re
import pyfrotz
from frotz.frotz_patch import patch_frotz
from util.file_utils import read_file


class Game:
    """Wrapper around Frotz with simplified interface."""

    def __init__(
        self,
        working_dir: str = ".",
        data_folder: str = "frotz/data",
        game_file: str = "zork1.z3",
    ):
        patch_frotz()

        self._base_folder = f"{working_dir}/{data_folder}"
        interpreter = self._find_interpreter()
        self.wrapper = pyfrotz.Frotz(
            f"{self._base_folder}/{game_file}",
            interpreter=interpreter,
            reformat_spacing=False,
        )
        self.has_quit = False

    def _find_interpreter(self) -> str:
        possible_interpreter_paths = [
            os.path.join(os.path.expanduser("~/.pyfrotz"), "dfrotz"),  # default
            os.path.join(os.path.expanduser("~/.pyfrotz"), "dfrotz.exe"),  # Windows
            "/opt/homebrew/bin/dfrotz",
            "/usr/local/bin/dfrotz",
            "/usr/bin/dfrotz",
            os.path.join(os.path.dirname(pyfrotz.__file__), "dfrotz"),
        ]

        for path in possible_interpreter_paths:
            if os.path.exists(path):
                return path

        return "dfrotz"

    def get_game_play_notes(self) -> str:
        return read_file(f"{self._base_folder}/Zork Gameplay Notes.txt")

    def get_intro(self) -> str:
        return self.wrapper.get_intro()

    def do_command(self, command: str) -> str:
        answer = self.wrapper.do_command(command)
        room, description = answer

        first = self._strip_whitespaces(room)
        second = self._strip_whitespaces(description)
        # TODO scan answer for "you are dead"
        if second:
            return f"{first}\n{second}"
        return first

    def _strip_whitespaces(self, text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

    def room_name(self) -> str:
        # available via patch
        return self.wrapper.derived_name  # pylint: disable=no-member

    def moves(self) -> int:
        return self.wrapper.derived_moves  # pylint: disable=no-member

    def score(self) -> int:
        return self.wrapper.derived_score  # pylint: disable=no-member

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
