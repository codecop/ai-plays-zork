"""Script to start the whole thing."""

import sys
from create_ai import create

# commandline arguments
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

# create and run application
application = create(CONFIG)
application.start()
application.run(THRESHOLD_SECONDS)
application.close()
