import pytest
from pathlib import Path
from src.file_utils import readFile, writeFile, getNextFolderName


def cleanup_test_data(test_dir):
    for item in test_dir.glob("*"):
        if item.is_dir():
            item.rmdir()
        else:
            item.unlink()
    test_dir.rmdir()


@pytest.fixture
def test_data_dir():
    """Fixture to create and clean up test directory"""
    test_dir = Path("test/data/file_utils/tmp")
    test_dir.mkdir(exist_ok=True)
    yield test_dir
    cleanup_test_data(test_dir)


def test_readFile():
    test_file_path = "test/data/file_utils/utf8-sample"
    content = readFile(test_file_path)
    assert content == "Two lines test content\nwith special chars äöüß\n"


def test_writeFile(test_data_dir):
    output_path = test_data_dir / "test_output.txt"
    test_output = "Test output with special chars: ñáéíóú"
    writeFile(str(output_path), test_output)

    assert output_path.exists()
    assert output_path.stat().st_size == 44


@pytest.mark.skip
def test_getNextFolderName(test_data_dir):
    """Test finding the next available folder name"""
    # Test with no existing folders
    next_name = getNextFolderName(str(test_data_dir), "test")
    assert next_name == "test-001"

    # Create some test folders
    test_dirs = ["test-001", "test-002", "test-005"]
    for d in test_dirs:
        (test_data_dir / d).mkdir(exist_ok=True)

    # Test with existing folders
    next_name = getNextFolderName(str(test_data_dir), "test")
    assert next_name == "test-006"
