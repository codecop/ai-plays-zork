from util.log import Log


class MemoryLog(Log):

    def __init__(self):
        self.ai_messages = []
        self.game_messages = []
        self.command_messages = []
        self.room_messages = []
        self.warn_messages = []

    def ai(self, text: str) -> None:
        self.ai_messages.append(text)

    def game(self, text: str) -> None:
        self.game_messages.append(text)

    def command(self, command: str) -> None:
        self.command_messages.append(command)

    def room(self, text: str) -> None:
        self.room_messages.append(text)

    def warn(self, text: str) -> None:
        self.warn_messages.append(text)
