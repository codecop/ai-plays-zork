import pytest
from pathlib import Path
from log import Log
from ai_interface import AiInterface
from test_file_utils import data_dir


class EmptyAi(AiInterface):
    """Empty implementation to test resource methods."""

    def start(self, game_notes: str, game_intro: str):
        assert false

    def get_next_command(self, context: str):
        assert false

    def close(self):
        assert false


@pytest.fixture
def ai(data_dir: Path) -> EmptyAi:
    run_path = data_dir
    log = Log(run_path)
    return EmptyAi("mistralai", run_path, log)


def test_resources(ai) -> None:
    assert ai.resource_dir().parts[-2] == "src"
    assert ai.resource_dir().parts[-1] == "mistralai"

    resource = ai.load_resource("system_prompt.md")
    assert resource.startswith("# Goal")


def test_run_resource(ai) -> None:
    file = "someFile.txt"
    assert not ai.exists_run_resource(file)
    ai.write_run_resource(file, "test")
    assert ai.exists_run_resource(file)
    assert ai.load_run_resource(file) == "test"
    ai.remove_run_resource(file)
    assert not ai.exists_run_resource(file)


def test_config_json(ai) -> None:
    assert ai.configuration == "mistralai"
    assert ai.config()["model"] == "mistral-small-latest"
    assert ai.config()["name"] == "Zork Agent"
    assert ai.config()["description"] == "AI adventurer playing Zork."
