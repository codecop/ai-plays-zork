from log import Log


class CompositeLog(Log):
    def __init__(self, *logs: Log):
        # super().__init__(path)  # pylint: disable=super-init-not-called
        self.logs = logs

    def ai(self, text: str) -> None:
        for log in self.logs:
            log.ai(text)

    def game(self, text: str) -> None:
        for log in self.logs:
            log.game(text)

    def command(self, command: str) -> None:
        for log in self.logs:
            log.command(command)

    def room(self, text: str) -> None:
        for log in self.logs:
            log.room(text)
