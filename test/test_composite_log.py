from memory_log import MemoryLog
from composite_log import CompositeLog


def test_composite_log_delegates_to_all_logs():
    fake_log1 = MemoryLog()
    fake_log2 = MemoryLog()
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
