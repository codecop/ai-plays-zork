import sys
from create_ai import create_ai
from run import run


# init AI
if len(sys.argv) > 1:
    config = sys.argv[1]
else:
    raise ValueError("No config provided")

ai = create_ai(config)
run(ai)
