from abc import ABC, abstractmethod
from pathlib import Path
from src.file_utils import readFile
from src.log import Log


class AiInterface(ABC):
    """Base class defining the interface for AI implementations."""

    def __init__(self, run_folder: Path, log: Log):
        self.run_folder = run_folder
        self.log = log

    @abstractmethod
    def name(self) -> str:
        """Return the name of the AI implementation."""
        pass

    def resource_dir(self) -> Path:
        return Path(__file__).parent / self.name()

    def load_resource(self, filename: str) -> str:
        """Load a text resource file from the AI's resource directory."""
        resource_file = self.resource_dir() / filename
        return readFile(resource_file)

    @abstractmethod
    def start(self, game_notes: str, game_intro: str) -> None:
        """Initialize the AI with game context."""
        pass

    @abstractmethod
    def get_next_command(self, context: str) -> str:
        """Get the next command from the AI based on the current game context.

        Args:
            context: The current game state/context.

        Returns:
            The next command to execute in the game.
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """Clean up any resources used by the AI."""
        pass
