# Claude Code MCP Setup for Zork

This directory contains the configuration and scripts to install the Zork MCP servers for Claude Code.

## Prerequisites

1. **uv** - Python package manager

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **frotz** - Z-machine interpreter

   ```bash
   # macOS
   brew install frotz

   # Ubuntu/Debian
   sudo apt-get install frotz

   # Fedora
   sudo dnf install frotz
   ```

## Installation

To install the Zork MCP servers into your Claude Code configuration:

```bash
python src/with_mcp/claude_setup/install_claude_mcp.py
```

This will:

- Add two MCP servers to your `~/.claude/mcp-servers.json`:
  - `zork-game` - Basic game server
  - `zork-game-with-logging` - Server with logging capabilities
- Automatically set the correct paths based on your repository location
- Preserve any existing MCP servers in your configuration

After installation, restart Claude Code to load the new servers.

## Uninstallation

To remove the Zork MCP servers from your Claude Code configuration:

```bash
python src/with_mcp/claude_setup/uninstall_claude_mcp.py
```

This will:

- Remove only the Zork-related MCP servers
- Leave other MCP servers untouched
- Clean up empty configuration files if needed

## Files

- `mcp-servers-zork.json` - The MCP server configuration template
- `install_claude_mcp.py` - Installation script
- `uninstall_claude_mcp.py` - Uninstallation script

## Usage in Claude Code

Once installed and Claude Code is restarted, the Zork game tools will be available. Claude can then use tools like:

- `send_command` - Send commands to the game
- `get_game_status` - Check current room, score, and moves
- `get_last_answer` - Review the last game response
- `get_gameplay_notes` - Read gameplay hints
