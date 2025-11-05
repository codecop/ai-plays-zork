# Repository Map (feel free to edit!)

## Root Level
- frotz/ - Game binary, pyFrotz Python wrapper, and installation files
- bin/ - Build and development scripts
- runs-archive/ - Archived AI game runs from different implementations
- windsurf_conversations/ - Saved Windsurf AI conversations
- test/ - Test files for all components

## src/ - Main Source Code
- ai/ - Different AI implementations (Claude Code, Mistral, OpenAI) for playing Zork
- frotz/ - Game interface with tmux scripts and MCP server setup
- mcp/ - MCP infrastructure, installation guides, and server implementations
- tools/ - Game map generation and room change detection
- util/ - Logging, file handling, and run management utilities
- with_loop/ - AI integrated directly in the game loop
- with_mcp/ - AI controls game via Model Context Protocol
- with_tool/ - Placeholder for future tool-based approach

## Approaches
- with_loop: AI is integrated into the game loop, feeding commands directly
- with_mcp: AI uses Model Context Protocol to control the game as an external tool
- with_tool: AI plays Zork using tools
