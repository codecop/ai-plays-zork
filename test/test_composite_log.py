from composite_log import CompositeLog
from log import Log


class FakeLog(Log):

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


def test_composite_log_delegates_to_all_logs():
    fake_log1 = FakeLog()
    fake_log2 = FakeLog()
    composite_log = CompositeLog(fake_log1, fake_log2)

    composite_log.ai("AI message")
    composite_log.game("Game message")
    composite_log.command("north")
    composite_log.room("You are in a room")
    composite_log.warn("Warning message")

    assert fake_log1.ai_messages == ["AI message"]
    assert fake_log1.game_messages == ["Game message"]
    assert fake_log1.command_messages == ["north"]
    assert fake_log1.room_messages == ["You are in a room"]
    assert fake_log1.warn_messages == ["Warning message"]

    assert fake_log2.ai_messages == ["AI message"]
    assert fake_log2.game_messages == ["Game message"]
    assert fake_log2.command_messages == ["north"]
    assert fake_log2.room_messages == ["You are in a room"]
    assert fake_log2.warn_messages == ["Warning message"]
