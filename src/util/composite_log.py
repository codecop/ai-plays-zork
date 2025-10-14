from util.log import Log


class CompositeLog(Log):
    """Log combining multiple logs as one."""

    def __init__(self, *logs: Log):
        super().__init__()
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

    def warn(self, text: str) -> None:
        for log in self.logs:
            log.warn(text)
