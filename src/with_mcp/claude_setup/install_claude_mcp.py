#!/usr/bin/env python

import json
import os
import sys
from pathlib import Path


def install_mcp_servers():
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent.parent.parent

    zork_config_path = script_dir / "mcp-servers-zork.json"
    claude_config_dir = Path.home() / ".claude"
    claude_config_path = claude_config_dir / "mcp-servers.json"

    if not zork_config_path.exists():
        print(f"Error: {zork_config_path} not found")
        return False

    with open(zork_config_path) as f:
        zork_config = json.load(f)

    for server_name, server_config in zork_config["mcpServers"].items():
        if "cwd" not in server_config:
            server_config["cwd"] = str(repo_root)

        if "env" in server_config and "PYTHONPATH" in server_config["env"]:
            if not os.path.isabs(server_config["env"]["PYTHONPATH"]):
                server_config["env"]["PYTHONPATH"] = str(
                    repo_root / server_config["env"]["PYTHONPATH"]
                )

    claude_config_dir.mkdir(parents=True, exist_ok=True)

    if claude_config_path.exists():
        with open(claude_config_path) as f:
            existing_config = json.load(f)

        if "mcpServers" not in existing_config:
            existing_config["mcpServers"] = {}

        for server_name, server_config in zork_config["mcpServers"].items():
            if server_name in existing_config["mcpServers"]:
                print(f"Warning: Overwriting existing server '{server_name}'")
            existing_config["mcpServers"][server_name] = server_config

        final_config = existing_config
        print("Merging Zork MCP servers into existing Claude configuration...")
    else:
        final_config = zork_config
        print("Creating new Claude MCP configuration...")

    with open(claude_config_path, "w") as f:
        json.dump(final_config, f, indent=2)

    print(f"✅ Successfully installed Zork MCP servers to {claude_config_path}")
    print("\nInstalled servers:")
    for server_name in zork_config["mcpServers"].keys():
        print(f"  - {server_name}")
    print(f"\nRepository root: {repo_root}")
    print("\n⚠️  Please restart Claude Code for changes to take effect")

    return True


if __name__ == "__main__":
    success = install_mcp_servers()
    sys.exit(0 if success else 1)
