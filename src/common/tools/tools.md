# Zork TMux Tools

Simple tools for playing Zork in a tmux session.

## Tools

### `launch_zork_session.sh`
Launches Zork in a named tmux session called "zork-game".
- Creates new session if none exists
- Attaches to existing session if already running
```bash
./tools/launch_zork_session.sh
```

### `send_command.sh`
Sends a command to Zork and displays the response.
```bash
./tools/send_command.sh "open mailbox"
./tools/send_command.sh "go north"
```

### `get_last_response.sh`
Gets the last command and response from the game.
- Shows initial state if no commands entered yet
- Returns only the most recent interaction
```bash
./tools/get_last_response.sh
```

## Typical Usage

```bash
# Terminal 1: Launch the game
./tools/launch_zork_session.sh

# Terminal 2: Play the game
./tools/send_command.sh "look"
./tools/send_command.sh "open mailbox"
./tools/send_command.sh "take leaflet"

# Or just check current state
./tools/get_last_response.sh
```

## Direct TMux Commands

```bash
# Kill the session when done
tmux kill-session -t zork-game

# Attach to session manually
tmux attach -t zork-game

# Detach from session
Ctrl+b, d
```