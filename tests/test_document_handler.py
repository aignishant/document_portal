import os
from pathlib import Path

import fitz
import pytest

from src.constants import ENV_DATA_STORAGE_PATH, ERR_PDF_NOT_FOUND, ERR_PDF_READ
from src.document_analysier.data_ingestion import AppException, DocumentHandler


class DummyFile:
    def __init__(self, path: Path):
        self.path = str(path)
        self.name = path.name

    def getbuffer(self):
        with open(self.path, "rb") as f:
            return f.read()


@pytest.fixture
def temp_data_dir(tmp_path, monkeypatch):
    """Fixture to provide a temporary data directory."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    monkeypatch.setenv(ENV_DATA_STORAGE_PATH, str(data_dir))
    return data_dir


@pytest.fixture
def sample_pdf(temp_data_dir):
    """Fixture to create a valid dummy PDF."""
    pdf_path = temp_data_dir / "sample.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Hello, World!")
    doc.save(pdf_path)
    doc.close()
    return pdf_path


def test_init_creates_session_dir(temp_data_dir):
    """Test that initializing DocumentHandler creates the session directory."""
    session_id = "test_session_123"
    handler = DocumentHandler(session_id=session_id)

    expected_path = temp_data_dir / session_id
    assert expected_path.exists()
    assert expected_path.is_dir()
    assert handler.session_id == session_id


def test_save_pdf_success(temp_data_dir, sample_pdf):
    """Test saving a PDF successfully."""
    handler = DocumentHandler()
    dummy = DummyFile(sample_pdf)
    saved_path = handler.save_pdf(dummy)

    assert os.path.exists(saved_path)
    # Compare content
    with open(sample_pdf, "rb") as f1, open(saved_path, "rb") as f2:
        assert f1.read() == f2.read()


def test_save_pdf_missing_file():
    """Test error when saving a non-existent file."""
    handler = DocumentHandler()
    dummy = DummyFile(Path("nonexistent.pdf"))
    with pytest.raises(AppException) as exc:
        handler.save_pdf(dummy)
    assert ERR_PDF_NOT_FOUND in str(exc.value)


def test_read_pdf_success(temp_data_dir, sample_pdf):
    """Test reading a PDF and extracting text."""
    handler = DocumentHandler()
    # Read the directly created sample PDF
    text = handler.read_pdf(str(sample_pdf))

    assert "Hello, World!" in text
    assert "--- Page 1  ---" in text


def test_read_pdf_failure():
    """Test error when reading an invalid or missing PDF."""
    handler = DocumentHandler()
    with pytest.raises(AppException) as exc:
        handler.read_pdf("nonexistent_file.pdf")
    assert ERR_PDF_READ in str(exc.value)
