import os
from pathlib import Path

import pytest

from src.constants import ERR_PDF_NOT_FOUND, ERR_PDF_READ
from src.document_analysier.data_ingestion import AppException, DocumentHandler
from tests.base import BaseTestCase


class TestDocumentHandler(BaseTestCase):

    def test_init_creates_session_dir(self, temp_data_dir):

        session_id = "test_session_123"

        handler = DocumentHandler(session_id=session_id)

        expected_path = temp_data_dir / session_id

        assert expected_path.exists()

        assert expected_path.is_dir()

        assert handler.session_id == session_id

    def test_save_pdf_success(self, temp_data_dir, sample_pdf, dummy_file_class):

        handler = DocumentHandler()

        dummy = dummy_file_class(sample_pdf)

        saved_path = handler.save_pdf(dummy)

        assert os.path.exists(saved_path)

        with open(sample_pdf, "rb") as f1, open(saved_path, "rb") as f2:

            assert f1.read() == f2.read()

    def test_save_pdf_missing_file(self, dummy_file_class):

        handler = DocumentHandler()

        dummy = dummy_file_class(Path("nonexistent.pdf"))

        with pytest.raises(AppException) as exc:

            handler.save_pdf(dummy)

        assert ERR_PDF_NOT_FOUND in str(exc.value)

    def test_read_pdf_success(self, temp_data_dir, sample_pdf):

        handler = DocumentHandler()

        text = handler.read_pdf(str(sample_pdf))

        assert "Hello, World!" in text

        assert "--- Page 1  ---" in text

    def test_read_pdf_failure(self):

        handler = DocumentHandler()

        with pytest.raises(AppException) as exc:

            handler.read_pdf("nonexistent_file.pdf")

        assert ERR_PDF_READ in str(exc.value)
