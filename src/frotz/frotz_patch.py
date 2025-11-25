"""Monkey patch Frotz to access the room name, score and moves."""

import re
import subprocess
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


def patched_get_frotz(self):
    import os
    if os.path.exists('/opt/homebrew/bin/dfrotz'):
        self.interpreter = '/opt/homebrew/bin/dfrotz'
    elif os.path.exists('/usr/local/bin/dfrotz'):
        self.interpreter = '/usr/local/bin/dfrotz'
    elif os.path.exists('/usr/bin/dfrotz'):
        self.interpreter = '/usr/bin/dfrotz'
    else:
        import pyfrotz
        package_dir = os.path.dirname(pyfrotz.__file__)
        self.interpreter = os.path.join(package_dir, 'dfrotz')

    self.frotz = subprocess.Popen([self.interpreter, self.data],
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

def patch_frotz():
    if Frotz._frotz_read != patched_frotz_read:
        Frotz._frotz_read = patched_frotz_read
    if Frotz._get_frotz != patched_get_frotz:
        Frotz._get_frotz = patched_get_frotz