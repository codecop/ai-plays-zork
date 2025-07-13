import pytest
from pathlib import Path
from log import Log
from test_file_utils import data_dir


@pytest.fixture
def log_file(data_dir: Path) -> (Log, Path):
    log_path = data_dir
    log = Log(log_path)
    return log, log.path


def test_log_creation(log_file) -> None:
    _, path = log_file
    assert path.exists()

    content = path.read_text(encoding="utf-8")
    assert content.startswith("START ")
    assert "GAME" not in content
    assert "CMD" not in content


def test_log_commands(log_file) -> None:
    log, path = log_file

    game_text = "You are in a dark forest."
    log.game(game_text)

    command = "look"
    log.command(command)

    content = path.read_text(encoding="utf-8")
    lines = content.strip().split("\n")
    assert len(lines) == 3  # START + game text + command
    assert lines[1] == f"GAME {game_text}"
    assert lines[2] == f"CMD {command}"


def test_multiline_log(log_file) -> None:
    log, path = log_file

    multi_line_text = "You are in a dark forest.\nThere is a path to the east."
    log.game(multi_line_text)

    content = path.read_text(encoding="utf-8")

    lines = content.strip().split("\n")
    assert lines[1] == "GAME You are in a dark forest."
    assert lines[2] == "     There is a path to the east."
