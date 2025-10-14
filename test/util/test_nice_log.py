from pathlib import Path
import pytest
from util.nice_log import NiceLog


@pytest.fixture(name="log_file")
def fixture_log_file(data_dir: Path) -> (NiceLog, Path):
    log_path = data_dir
    log = NiceLog(log_path)
    return log, log.path


def test_log_creation(log_file) -> None:
    _, path = log_file
    assert path.exists()

    content = path.read_text(encoding="utf-8")
    assert content.startswith("START ")
    assert "AI" not in content
    assert "CMD" not in content
    assert "GAME" not in content


def test_log_commands(log_file) -> None:
    log, path = log_file

    game_text = "You are in a dark forest."
    log.game(game_text)

    command = "look"
    log.command(command)

    ai = "AI response"
    log.ai(ai)

    room = "Kitchen"
    log.room(room)

    warn = "Warning"
    log.warn(warn)

    content = path.read_text(encoding="utf-8")
    lines = content.strip().split("\n")
    assert len(lines) == 6  # START + game text + command + ai + room + warn
    assert lines[1] == f"GAME  {game_text}"
    assert lines[2] == f"CMD   {command}"
    assert lines[3] == f"AI    {ai}"
    assert lines[4] == f"ROOM  {room}"
    assert lines[5] == f"WARN  {warn}"


def test_multiline_log(log_file) -> None:
    log, path = log_file

    multi_line_text = "You are in a dark forest.\nThere is a path to the east."
    log.game(multi_line_text)

    content = path.read_text(encoding="utf-8")

    lines = content.strip().split("\n")
    assert lines[1] == "GAME  You are in a dark forest."
    assert lines[2] == "      There is a path to the east."
