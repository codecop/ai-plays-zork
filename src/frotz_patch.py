import re
from pyfrotz import Frotz


def patched_extract_room_name(self, output):
    headline_re = re.compile(r"^\s*(.*)\s+Score: (\d+)\s+Moves: (\d+)")
    headline_match = headline_re.search(output)

    if headline_match:
        self.derived_name = headline_match.group(1).strip()
        self.derived_score = int(headline_match.group(2))
        self.derived_moves = int(headline_match.group(3))


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
    while output[-1] != ">":
        output += self.frotz.stdout.read(1).decode()

    # patch start
    patched_extract_room_name(self, output)
    # patch end

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


def patch_frotz():
    if Frotz._frotz_read != patched_frotz_read:  # pylint: disable=protected-access,comparison-with-callable
        Frotz._frotz_read = patched_frotz_read  # pylint: disable=protected-access
