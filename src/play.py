import sys
from create_ai import create_ai
from run import run

# init AI
if len(sys.argv) > 1:
    config = sys.argv[1]
else:
    print("Usage: python src/play.py config [threshold_seconds]")
    sys.exit(0)

if len(sys.argv) > 2:
    threshold_seconds = float(sys.argv[2])
else:
    threshold_seconds = 0


ai = create_ai(config)
run(ai, threshold_seconds)
