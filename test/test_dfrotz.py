import os
import subprocess


# Write a Python program to interact with Frotz. (curtesy Peter Fichtner)
def test_dfrotz_subprocess():

    frotz_path = os.path.expanduser('~/.pyfrotz/dfrotz')
    process = subprocess.Popen(
        [frotz_path, "-p", "data/zork1.z3"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    while True:
        line = process.stdout.readline().rstrip()
        print('> "' + line + '"', flush=True)
        if line == "There is a small mailbox here.":
            break
    assert line == "There is a small mailbox here."

    process.stdin.write("quit")
    process.stdin.write("y")
    process.stdin.flush()
