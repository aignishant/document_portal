from src.constants import ENV_DATA_STORAGE_PATH
import pytest
import fitz
import os
import sys
from pathlib import Path

# Add project root to sys.path before importing from src
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


class DummyFile:

    def __init__(self, path: Path):

        self.path = str(path)

        self.name = path.name

    def getbuffer(self):

        with open(self.path, "rb") as f:

            return f.read()


@pytest.fixture
def dummy_file_class():

    return DummyFile


@pytest.fixture
def temp_data_dir(tmp_path, monkeypatch):

    data_dir = tmp_path / "data"

    data_dir.mkdir()

    monkeypatch.setenv(ENV_DATA_STORAGE_PATH, str(data_dir))

    return data_dir


@pytest.fixture
def sample_pdf(temp_data_dir):

    pdf_path = temp_data_dir / "sample.pdf"

    doc = fitz.open()

    page = doc.new_page()

    page.insert_text((50, 50), "Hello, World!")

    doc.save(pdf_path)

    doc.close()

    return pdf_path
