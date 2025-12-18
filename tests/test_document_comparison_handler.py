import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from AIFoundationKit.base.exception.custom_exception import AppException

from src.document_comparison.document_handler import DocumentComparisonHandler
from tests.base import BaseTestCase


class TestDocumentComparisonHandler(BaseTestCase):

    @pytest.fixture
    def temp_doc_dir(self, tmp_path):

        doc_dir = tmp_path / "doc_data"

        doc_dir.mkdir()

        return doc_dir

    @pytest.fixture
    def doc_handler(self, temp_doc_dir):

        return DocumentComparisonHandler(
            session_id="test_session", file_path=str(temp_doc_dir)
        )

    def test_init_creates_directory(self, tmp_path):

        doc_dir = tmp_path / "new_doc_data"

        assert not doc_dir.exists()

        DocumentComparisonHandler(session_id="test_session", file_path=str(doc_dir))

        assert doc_dir.exists()

        assert doc_dir.is_dir()

    def test_init_default_directory(self):

        with patch("pathlib.Path.mkdir") as mock_mkdir:

            DocumentComparisonHandler(session_id="test_session")

            mock_mkdir.assert_called()

    def test_delete_existing_files(self, doc_handler, temp_doc_dir):

        (temp_doc_dir / "file1.txt").write_text("content1")

        (temp_doc_dir / "file2.pdf").write_bytes(b"content2")

        assert len(list(temp_doc_dir.iterdir())) == 3

        doc_handler.delete_existing_files()

        assert len(list(temp_doc_dir.iterdir())) == 1

    def test_save_file_path_input(self, doc_handler, temp_doc_dir, tmp_path):

        source_ref = tmp_path / "source_ref.txt"

        source_ref.write_text("reference content")

        source_act = tmp_path / "source_act.txt"

        source_act.write_text("actual content")

        ref_path, act_path = doc_handler.save_file(
            reference_file=str(source_ref), actual_file=str(source_act)
        )

        assert os.path.exists(ref_path)

        assert os.path.exists(act_path)

        assert Path(ref_path).read_text() == "reference content"

        assert Path(act_path).read_text() == "actual content"

        assert Path(ref_path).parent == temp_doc_dir

    def test_save_file_bytes_input(self, doc_handler):

        ref_content = b"reference bytes"

        act_content = b"actual bytes"

        ref_path, act_path = doc_handler.save_file(
            reference_file=ref_content,
            actual_file=act_content,
            reference_file_name="ref.bin",
            actual_file_name="act.bin",
        )

        assert os.path.exists(ref_path)

        assert os.path.exists(act_path)

        assert Path(ref_path).read_bytes() == ref_content

        assert Path(act_path).read_bytes() == act_content

        assert Path(ref_path).name == "ref.bin"

    def test_save_file_clears_previous(self, doc_handler, temp_doc_dir, tmp_path):

        (temp_doc_dir / "old_file.txt").write_text("old content")

        source_ref = tmp_path / "source_ref.txt"

        source_ref.write_text("new content")

        doc_handler.save_file(
            reference_file=str(source_ref),
            actual_file=str(source_ref),
            reference_file_name="new_ref.txt",
            actual_file_name="new_act.txt",
        )

        assert not (temp_doc_dir / "old_file.txt").exists()

        assert (temp_doc_dir / "new_ref.txt").exists()

    def test_save_file_not_found(self, doc_handler):

        with pytest.raises(AppException) as excinfo:

            doc_handler.save_file(
                reference_file="non_existent_file.txt",
                actual_file="another_non_existent.txt",
            )

        assert "Source file not found" in str(excinfo.value)

    @patch("src.document_comparison.document_handler.BaseFileManager")
    def test_read_file_success(self, mock_file_manager_cls, doc_handler):

        mock_instance = mock_file_manager_cls.return_value

        mock_instance.read_file.return_value = "file content"

        doc_handler.file_manager = MagicMock()

        doc_handler.file_manager.read_file.return_value = "file content"

        content = doc_handler.read_file("some/path/file.txt")

        assert content == "file content"

        doc_handler.file_manager.read_file.assert_called_once_with("some/path/file.txt")

    def test_read_file_failure(self, doc_handler):

        doc_handler.file_manager = MagicMock()

        doc_handler.file_manager.read_file.side_effect = Exception("Read error")

        with pytest.raises(AppException) as excinfo:

            doc_handler.read_file("some/path/file.txt")

        assert "Failed to read file" in str(excinfo.value)
