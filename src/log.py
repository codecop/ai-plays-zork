from abc import ABC, abstractmethod


class Log(ABC):
    """Base class of all logs."""

    @abstractmethod
    def ai(self, text: str) -> None:
        pass

    @abstractmethod
    def game(self, text: str) -> None:
        pass

    @abstractmethod
    def command(self, command: str) -> None:
        pass

    @abstractmethod
    def room(self, text: str) -> None:
        pass
