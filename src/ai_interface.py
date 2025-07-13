from abc import ABC, abstractmethod
from pathlib import Path

from file_utils import readFile


class AiInterface(ABC):
    """Base class defining the interface for AI implementations."""

    @abstractmethod
    def name(self) -> str:
        """Return the name of the AI implementation."""
        pass

    def load_resource(self, filename: str) -> str:
        """Load a text resource file from the AI's resource directory."""
        resource_dir = Path(__file__).parent / self.name()
        resource_file = resource_dir / filename
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
