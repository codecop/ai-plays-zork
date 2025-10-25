# Install MCP into Windsurf

Windsurf supports two transport types for MCP servers: stdio and http/websocket.

Example configurations:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-github"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<YOUR_PERSONAL_ACCESS_TOKEN>"
      }
    }
  }
}
```

```json
{
  "mcpServers": {
    "figma": {
      "serverUrl": "<your-server-url>/mcp"
    }
  }
}
```

Restart Windsurf or reload the MCP connection.
