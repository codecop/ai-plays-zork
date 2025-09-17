#!/bin/bash

# Get the last command and response from the zork-game tmux session
# Returns only the most recent interaction (between last two > prompts)

SESSION_NAME="zork-game"

# Check if session exists
if ! tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo "Error: No session '$SESSION_NAME' found. Run ./tools/launch_zork_session.sh first" >&2
    exit 1
fi

# Extract the last command and its response
output=$(tmux capture-pane -t "$SESSION_NAME" -p | perl -0ne 'print $1 if />([^>]+)>?$/s')

if [ -z "$output" ]; then
    # No commands entered yet, show initial game state (last 15 lines before prompt)
    tmux capture-pane -t "$SESSION_NAME" -p | tail -15 | sed '$d'
else
    echo "$output"
fi