from pathlib import Path
import pytest
from file_utils import read_file, write_file, next_folder_name


def cleanup_test_data(data_dir: Path) -> None:
    for item in data_dir.glob("*"):
        if item.is_dir():
            item.rmdir()
        else:
            item.unlink()
    data_dir.rmdir()


@pytest.fixture(name="data_dir")
def fixture_data_dir() -> Path:
    """Fixture to create and clean up test directory"""
    data_dir = Path("./test/data/tmp")
    data_dir.mkdir(exist_ok=True)
    yield data_dir
    cleanup_test_data(data_dir)


def test_read_file() -> None:
    test_file = "test/data/file_utils/utf8-sample"
    content = read_file(test_file)

    assert content == "Two lines test content\nwith special chars äöüß\n"


def test_write_file(data_dir: Path) -> None:
    output_path = data_dir / "test_output.txt"
    test_output = "Test output with special chars: ñáéíóú"
    write_file(str(output_path), test_output)

    assert output_path.exists()
    assert output_path.stat().st_size == 44


def test_next_folder_name_new(data_dir: Path) -> None:
    next_folder = next_folder_name(data_dir, "test")
    assert next_folder.name == "test-001"
    assert next_folder.exists()


def test_next_folder_name_existing(data_dir: Path) -> None:
    # Create some test folders
    test_dirs = ["test-001", "test-002", "test-005", "other"]
    for test_dir in test_dirs:
        (data_dir / test_dir).mkdir(exist_ok=True)

    next_dir = next_folder_name(data_dir, "test")
    assert next_dir.parts[-1] == "test-006"
