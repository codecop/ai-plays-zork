# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project implements an AI that plays the classic text adventure game Zork I. The AI uses the Mistral API to make decisions and interacts with the game through the pyFrotz library (a Python wrapper for the Frotz Z-machine interpreter).

## Development Commands

### Running the main application

```bash
python src/play.py
```

### Running tests

```bash
pytest
# or for verbose output with pytest.ini configuration
pytest -v -ra
```

### Installing dependencies

```bash
pip install -r requirements.txt
```

## Environment Setup

The application requires a `MISTRAL_API_KEY` environment variable to be set for the AI functionality.

## Architecture Overview

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────┐
│   src/play.py   │───▶│   Game       │───▶│   pyFrotz   │
│  (main loop)    │    │  (wrapper)   │    │ (Z-machine) │
└─────────────────┘    └──────────────┘    └─────────────┘
         │                      │
         ▼                      ▼
┌─────────────────┐    ┌──────────────┐
│   MistralAi     │    │     Log      │
│ (AI decisions)  │    │ (recording)  │
└─────────────────┘    └──────────────┘
         │
         ▼
┌─────────────────┐
│  AiInterface    │
│ (base class)    │
└─────────────────┘
```

### Core Components

- **Game** (`src/game.py`): Wraps pyFrotz to provide a clean interface to the Zork game engine
- **MistralAi** (`src/mistral_ai.py`): Implements the AI player using Mistral's agent API
- **AiInterface** (`src/ai_interface.py`): Abstract base class defining the AI contract
- **Log** (`src/log.py`): Handles console output with color coding and file logging
- **play.py**: Main game loop that coordinates between the AI and the game

### Game Flow

1. Initialize a new run folder for logging
2. Start the game and get intro/notes
3. Initialize AI with game context
4. Main loop:
   - Send command to game
   - Log game response
   - Get AI's next command based on game output
   - Log AI command
   - Repeat until game ends

## Key Implementation Details

- **Run Management**: Each game session creates a numbered run folder (e.g., `mistralai-run-001/`) for isolated logging
- **AI Context**: The AI receives both gameplay notes and the game intro as initial context
- **Command Processing**: The game wrapper strips whitespace and handles multi-line responses
- **Logging**: All interactions are logged both to console (with colors) and to `log.txt` in the run folder

## File Structure

- `src/`: Main source code
- `test/`: Test files using pytest
- `data/`: Game files and gameplay notes
- `frotz/`: Contains pyFrotz library and dfrotz executable
- `[config]-run-*/`: Generated run folders with logs and AI context

## Testing

Tests are configured via `pytest.ini` with:

- Verbose output (`-v`)
- Summary of all results (`-ra`)
- Source paths include both `src` and `test`
- Test discovery pattern: `test_*.py`