
import os
import shutil
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from rag_common.exception.custom_exception import AppException
from src.document_comparison.document_handler import DocumentComparisonHandler


@pytest.fixture
def temp_doc_dir(tmp_path):
    """Fixture to provide a temporary directory for document storage."""
    doc_dir = tmp_path / "doc_data"
    doc_dir.mkdir()
    return doc_dir


@pytest.fixture
def doc_handler(temp_doc_dir):
    """Fixture to provide a valid DocumentComparisonHandler instance."""
    return DocumentComparisonHandler(session_id="test_session", file_path=str(temp_doc_dir))


def test_init_creates_directory(tmp_path):
    """Test that initialization creates the specified directory."""
    doc_dir = tmp_path / "new_doc_data"
    assert not doc_dir.exists()

    DocumentComparisonHandler(session_id="test_session", file_path=str(doc_dir))

    assert doc_dir.exists()
    assert doc_dir.is_dir()


def test_init_default_directory():
    """Test initialization with default directory logic (mocking project root to avoid clutter)."""
    # This is harder to test without mocking the project root resolution logic in the class,
    # but we can at least ensure it doesn't crash.
    # We'll use a patch to ensuring we don't actually write to the real 'data' folder for this test
    with patch("pathlib.Path.mkdir") as mock_mkdir:
        DocumentComparisonHandler(session_id="test_session")
        mock_mkdir.assert_called()


def test_delete_existing_files(doc_handler, temp_doc_dir):
    """Test that existing files are deleted."""
    # Create some dummy files
    (temp_doc_dir / "file1.txt").write_text("content1")
    (temp_doc_dir / "file2.pdf").write_bytes(b"content2")

    assert len(list(temp_doc_dir.iterdir())) == 2

    doc_handler.delete_existing_files()

    assert len(list(temp_doc_dir.iterdir())) == 0


def test_save_file_path_input(doc_handler, temp_doc_dir, tmp_path):
    """Test saving files when input is a file path."""
    # Create source files
    source_ref = tmp_path / "source_ref.txt"
    source_ref.write_text("reference content")
    source_act = tmp_path / "source_act.txt"
    source_act.write_text("actual content")

    ref_path, act_path = doc_handler.save_file(
        reference_file=str(source_ref),
        actual_file=str(source_act)
    )

    assert os.path.exists(ref_path)
    assert os.path.exists(act_path)
    assert Path(ref_path).read_text() == "reference content"
    assert Path(act_path).read_text() == "actual content"
    assert Path(ref_path).parent == temp_doc_dir


def test_save_file_bytes_input(doc_handler, temp_doc_dir):
    """Test saving files when input is bytes."""
    ref_content = b"reference bytes"
    act_content = b"actual bytes"

    ref_path, act_path = doc_handler.save_file(
        reference_file=ref_content,
        actual_file=act_content,
        reference_file_name="ref.bin",
        actual_file_name="act.bin"
    )

    assert os.path.exists(ref_path)
    assert os.path.exists(act_path)
    assert Path(ref_path).read_bytes() == ref_content
    assert Path(act_path).read_bytes() == act_content
    assert Path(ref_path).name == "ref.bin"


def test_save_file_clears_previous(doc_handler, temp_doc_dir, tmp_path):
    """Test that saving new files clears the directory first."""
    # First save
    (temp_doc_dir / "old_file.txt").write_text("old content")

    source_ref = tmp_path / "source_ref.txt"
    source_ref.write_text("new content")

    doc_handler.save_file(
        reference_file=str(source_ref),
        actual_file=str(source_ref),  # Using same for simplicity
        reference_file_name="new_ref.txt",
        actual_file_name="new_act.txt"
    )

    # Old file should be gone
    assert not (temp_doc_dir / "old_file.txt").exists()
    # New files should exist
    assert (temp_doc_dir / "new_ref.txt").exists()


def test_save_file_not_found(doc_handler):
    """Test error handling when source file doesn't exist."""
    with pytest.raises(AppException) as excinfo:
        doc_handler.save_file(
            reference_file="non_existent_file.txt",
            actual_file="another_non_existent.txt"
        )
    assert "Source file not found" in str(excinfo.value)


@patch("src.document_comparison.document_handler.read_any_file")
def test_read_file_success(mock_read_any_file, doc_handler):
    """Test successfully reading a file."""
    mock_read_any_file.return_value = "file content"

    content = doc_handler.read_file("some/path/file.txt")

    assert content == "file content"
    mock_read_any_file.assert_called_once_with("some/path/file.txt")


@patch("src.document_comparison.document_handler.read_any_file")
def test_read_file_failure(mock_read_any_file, doc_handler):
    """Test failure during file read."""
    mock_read_any_file.side_effect = Exception("Read error")

    with pytest.raises(AppException) as excinfo:
        doc_handler.read_file("some/path/file.txt")

    assert "Failed to read file" in str(excinfo.value)
