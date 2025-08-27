import re
from pyfrotz import Frotz
from file_utils import read_file

def patched_frotz_read(self, parse_room=True):
    """
        Read from frotz interpreter process.
        Returns tuple with Room name and description.
    """
    # Read room info
    output = ""
    output += self.frotz.stdout.read(1).decode()
    if not len(output):
        return ""
    while output[-1] != '>':
        output += self.frotz.stdout.read(1).decode()

    # get score moves and names from output
    score_move_re = re.compile(r'^\s*(.*)\s+Score: (\d+)\s+Moves: (\d+)')
    score_move_match = score_move_re.search(output)
    if score_move_match:
        self.derived_name = score_move_match.group(1).strip()
        self.derived_score = int(score_move_match.group(2))
        self.derived_moves = int(score_move_match.group(3))
        # print(f"Name: {self.derived_name}, Score: {self.derived_score}, Moves: {self.derived_moves}")

    lines = [l for l in output[:-1].split("\n") if l.strip() and "Score: " not in l]
    if parse_room:
        room = lines[0]
        lines = lines[1:]
    # reformat text by . instead of \n
    if self.reformat_spacing:
        lines = " ".join(lines).replace(".", ".\n")
    else:
        lines = "\n".join(lines)
    # Return description removing the prompt
    if parse_room:
        return room, lines
    return lines

class Game:
    def __init__(self, game_file: str = "data/zork1.z3"):
        Frotz._frotz_read = patched_frotz_read
        self.wrapper = Frotz(game_file)
        self.has_quit = False

    def get_game_play_notes(self) -> str:
        return read_file("data/Zork Gameplay Notes.txt")

    def get_intro(self) -> str:
        return self.wrapper.get_intro()

    def do_command(self, command: str) -> str:
        answer = self.wrapper.do_command(command)
        room, description = answer

        first = self.strip_whitespaces(room)
        second = self.strip_whitespaces(description)
        # TODO scan answer for "you are dead"
        if second:
            return f"{first}\n{second}"
        return first

    def strip_whitespaces(self, text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

    def room_name(self) -> str:
        return self.wrapper.derived_name

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
