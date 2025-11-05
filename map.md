# Repository Map (feel free to edit!)

## Root Level

- bin/ - Build and development scripts, tool configurations
- frotz/ - Game binary, pyFrotz Python wrapper, and installation files
- runs/ - Temporary data of AI game runs from different implementations
- runs-archive/ - Archived AI game runs from different implementations
- src/ - Main source files
- test/ - Test files for all components
- windsurf_conversations/ - Saved Windsurf AI conversations

## src/ - Main Source Code

- ai/ - Different AI implementations (Claude Code, Mistral, OpenAI) for playing Zork
- frotz/ - Game interface with tmux scripts and MCP server setup
- mcp/ - MCP infrastructure, installation guides, and server prototypes
- tools/ - Game map generation and room change detection
- util/ - Logging, file handling, and run management utilities
- with_loop/ - AI integrated directly in the game loop (first approach)
- with_mcp/ - AI controls game via Model Context Protocol (second approach)
- with_tool/ - Placeholder for future tool-based approach (to be done)

## Approaches

- with_loop: AI is integrated into the game loop, feeding commands directly
- with_mcp: AI uses Model Context Protocol to control the game as an external tool
- with_tool: AI plays Zork using tools
