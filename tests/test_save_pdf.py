import os
import shutil
from pathlib import Path
import pytest

from src.document_analysier.data_ingestion import DocumentHandler, AppException

class DummyFile:
    def __init__(self, path: Path):
        self.path = str(path)
        self.name = path.name
    def getbuffer(self):
        with open(self.path, "rb") as f:
            return f.read()

@pytest.fixture
def temp_data_dir(tmp_path, monkeypatch):
    # Set DATA_STORAGE_PATH to a temporary directory
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    monkeypatch.setenv("DATA_STORAGE_PATH", str(data_dir))
    return data_dir

def test_save_pdf_success(temp_data_dir):
    # Create a temporary PDF file
    pdf_content = b"%PDF-1.4\n%Test PDF content"
    pdf_path = temp_data_dir / "sample.pdf"
    pdf_path.write_bytes(pdf_content)

    handler = DocumentHandler()
    dummy = DummyFile(pdf_path)
    saved_path = handler.save_pdf(dummy)

    # Verify the file was copied to the session directory
    assert os.path.exists(saved_path)
    with open(saved_path, "rb") as f:
        assert f.read() == pdf_content

def test_save_pdf_missing_file(temp_data_dir):
    handler = DocumentHandler()
    dummy = DummyFile(Path("nonexistent.pdf"))
    with pytest.raises(AppException) as exc:
        handler.save_pdf(dummy)
    assert "PDF file not found" in str(exc.value)
