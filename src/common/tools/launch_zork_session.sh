#!/bin/bash

# Launch Zork in a named tmux session
# This script creates or attaches to a tmux session named "zork-game"

SESSION_NAME="zork-game"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# Check if session already exists
if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo "Session '$SESSION_NAME' already exists."
    echo "Attaching to existing session..."
    tmux attach-session -t "$SESSION_NAME"
else
    echo "Creating new tmux session '$SESSION_NAME' with Zork..."
    echo "Project directory: $PROJECT_DIR"

    # Create new session and attach to it
    # Use full paths and run directly with bash
    tmux new-session -s "$SESSION_NAME" -c "$PROJECT_DIR" "bash -c '~/.pyfrotz/dfrotz data/zork1.z3'"
fi