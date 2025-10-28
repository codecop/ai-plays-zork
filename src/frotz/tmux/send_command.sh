#!/bin/bash

# Send a command to the zork-game tmux session
# Usage: ./send_command.sh "command"

SESSION_NAME="zork-game"

# Check if session exists
if ! tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo "Error: No session '$SESSION_NAME' found. Run ./launch_zork_session.sh first" >&2
    exit 1
fi

# Check if command provided
if [ -z "$1" ]; then
    echo "Usage: $0 \"command\""
    echo "Example: $0 \"open mailbox\""
    exit 1
fi

# Send the command
tmux send-keys -t "$SESSION_NAME" "$1" C-m

# Wait a bit for game to process
sleep 0.5

# Show the result
SCRIPT_DIR=$(dirname "$0" | tr -d '\r')
"$SCRIPT_DIR/get_last_response.sh"
