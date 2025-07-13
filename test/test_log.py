import pytest
from src.log import Log
from test.test_file_utils import data_dir


@pytest.fixture
def log_file(data_dir):
    log_path = data_dir
    return Log(str(log_path)), log_path / "log.txt"


def test_log_creation(log_file):
    _, path = log_file
    assert path.exists()

    content = path.read_text(encoding="utf-8")
    assert content.startswith("START ")
    assert "GAME" not in content
    assert "CMD" not in content


def test_log_commands(log_file):
    log, path = log_file

    game_text = "You are in a dark forest."
    log.gameText(game_text)

    command = "look"
    log.command(command)

    content = path.read_text(encoding="utf-8")
    lines = content.strip().split("\n")
    assert len(lines) == 3  # START + game text + command
    assert lines[1] == f"GAME {game_text}"
    assert lines[2] == f"CMD {command}"
