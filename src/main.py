import sys
from create_ai import create
from run_game_loop import run

CONFIG = None
THRESHOLD_SECONDS = None

if len(sys.argv) > 1:
    CONFIG = sys.argv[1]
else:
    print("Usage: python src/play.py config [threshold_seconds]")
    sys.exit(0)

if len(sys.argv) > 2:
    THRESHOLD_SECONDS = float(sys.argv[2])
else:
    THRESHOLD_SECONDS = 0


run_folder, log, ai = create(CONFIG)
run(run_folder, log, ai, THRESHOLD_SECONDS)
