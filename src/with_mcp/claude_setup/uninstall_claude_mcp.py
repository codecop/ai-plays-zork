#!/usr/bin/env python3

import json
import os
import sys
from pathlib import Path

def uninstall_mcp_servers():
    claude_config_path = Path.home() / ".claude" / "mcp-servers.json"

    if not claude_config_path.exists():
        print("No Claude MCP configuration found. Nothing to uninstall.")
        return True

    with open(claude_config_path) as f:
        config = json.load(f)

    if "mcpServers" not in config:
        print("No MCP servers configured. Nothing to uninstall.")
        return True

    zork_servers = ["zork-game", "zork-game-with-logging"]
    removed_servers = []

    for server_name in zork_servers:
        if server_name in config["mcpServers"]:
            del config["mcpServers"][server_name]
            removed_servers.append(server_name)

    if not removed_servers:
        print("No Zork MCP servers found in configuration.")
        return True

    if not config["mcpServers"]:
        if len(config) == 1:
            claude_config_path.unlink()
            print(f"Removed empty configuration file: {claude_config_path}")
        else:
            del config["mcpServers"]
            with open(claude_config_path, "w") as f:
                json.dump(config, f, indent=2)
    else:
        with open(claude_config_path, "w") as f:
            json.dump(config, f, indent=2)

    print(f"✅ Successfully uninstalled Zork MCP servers from {claude_config_path}")
    print("\nRemoved servers:")
    for server_name in removed_servers:
        print(f"  - {server_name}")
    print("\n⚠️  Please restart Claude Code for changes to take effect")

    return True

if __name__ == "__main__":
    success = uninstall_mcp_servers()
    sys.exit(0 if success else 1)