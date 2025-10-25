"""Script to start the whole thing."""

import sys
from with_loop.create_loop_ai import create

# commandline arguments
CONFIG = None
LOOPS_KEY = "-loops="
MAX_LOOPS = 1000
for arg in sys.argv:
    if arg.startswith(LOOPS_KEY):
        MAX_LOOPS = int(arg[len(LOOPS_KEY) :])
        break

THRESHOLD_KEY = "-threshold="
THRESHOLD_SECONDS = 0.0
for arg in sys.argv:
    if arg.startswith(THRESHOLD_KEY):
        THRESHOLD_SECONDS = float(arg[len(THRESHOLD_KEY) :])
        break

if len(sys.argv) > 1:
    CONFIG = sys.argv[1]
else:
    print(
        "Usage: python src/main.py config "
        + f"[{LOOPS_KEY}max_loops|{MAX_LOOPS}] "
        + f"[{THRESHOLD_KEY}threshold_seconds|{THRESHOLD_SECONDS}]"
    )
    sys.exit(0)


# create and run application
application = create(CONFIG)
application.start()

try:
    application.run(MAX_LOOPS, THRESHOLD_SECONDS)
except KeyboardInterrupt:
    pass
finally:
    application.close()
