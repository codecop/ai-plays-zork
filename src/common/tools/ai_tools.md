# Zork TMux Tools

Simple tools for playing Zork. Assume Zork is launched in a named tmux session called "zork-game".

## Tools

### `send_command.sh`
Sends a command to Zork and displays the response.
```bash
./src/common/tools/send_command.sh "open mailbox"
./src/common/tools/send_command.sh "go north"
```

### `get_last_response.sh`
Gets the last command and response from the game.
- Shows initial state if no commands entered yet
- Returns only the most recent interaction
```bash
./src/common/tools/get_last_response.sh
```

## Typical Usage

```bash
# Play the game
./src/common/tools/send_command.sh "look"
./src/common/tools/send_command.sh "open mailbox"
./src/common/tools/send_command.sh "take leaflet"

# Check current state
./src/common/tools/get_last_response.sh
```
