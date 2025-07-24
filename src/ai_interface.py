from abc import ABC, abstractmethod
from pathlib import Path
from file_utils import readFile, writeFile
from log import Log


class AiInterface(ABC):
    """Base class defining the interface for AI implementations."""

    def __init__(self, configuration: str, run_folder: Path, log: Log):
        self.configuration = configuration
        self.run_folder = run_folder
        self.log = log

    def resource_dir(self) -> Path:
        return Path(__file__).parent / self.configuration

    def load_resource(self, filename: str) -> str:
        """Load a text resource file from the AI's resource directory."""
        resource_file = self.resource_dir() / filename
        return readFile(resource_file)

    def load_resource(self, filename: str) -> str:
        """Load a text resource file from the AI's resource directory."""
        resource_file = self.resource_dir() / filename
        return readFile(resource_file)

    def load_run_resource(self, filename: str) ->  str:
        target_file = self.run_folder / filename
        return readFile(target_file)

    def write_run_resource(self, filename: str, content: str) -> None:
        target_file = self.run_folder / filename
        writeFile(target_file, content)

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
