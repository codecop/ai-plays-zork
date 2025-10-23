from pathlib import Path
import pytest


def cleanup_test_data(data_dir: Path) -> None:
    for item in data_dir.glob("*"):
        if item.is_dir():
            item.rmdir()
        else:
            item.unlink()
    data_dir.rmdir()


@pytest.fixture(name="data_dir")
def fixture_data_dir() -> Path:
    data_dir = Path("./test/data_tmp")
    data_dir.mkdir(exist_ok=True)
    yield data_dir
    cleanup_test_data(data_dir)
