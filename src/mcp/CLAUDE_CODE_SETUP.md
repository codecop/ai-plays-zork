# Claude Code MCP Server Setup

## Quick Start

To add this MCP server to Claude Code, run:

```bash
claude mcp add --transport stdio zork-tools python <path-to-repo>/mcp/server.py
```

Replace `<path-to-repo>` with the absolute path to your ai-plays-zork repository.

## Verify Installation

Check that the server is connected:

```bash
claude mcp list
```

You should see:
```
zork-tools: python <path-to-repo>/mcp/server.py - ✓ Connected
```

## Inside Claude Code

Once configured, you can verify the MCP server is available by running the `/mcp` command within Claude Code.

## Removing the Server

If you need to remove the server:

```bash
claude mcp remove zork-tools
```

## Troubleshooting

- MCP servers are configured per-project by default (local scope)
- The configuration is stored in `~/.claude.json`
- No restart of Claude Code is needed after adding stdio servers
- Make sure Python is available in your PATH