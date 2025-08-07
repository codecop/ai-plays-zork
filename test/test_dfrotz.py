import os
import subprocess


# Write a Python program to interact with Frotz. (curtesy Peter Fichtner)
def test_frotz_subprocess():

    frotz_path = os.path.expanduser("~/.pyfrotz/dfrotz")

    with subprocess.Popen(
        [frotz_path, "-p", "data/zork1.z3"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    ) as frotz:

        while True:
            line = frotz.stdout.readline().rstrip()
            print('> "' + line + '"', flush=True)
            if line == "There is a small mailbox here.":
                break
        assert line == "There is a small mailbox here."

        # quit game
        frotz.stdin.write("quit")
        frotz.stdin.write("y")
        frotz.stdin.flush()

    # close all resources
    frotz.stdin.close()
    frotz.stdout.close()
    frotz.wait()
