import os
import sys
from pathlib import Path

from src.document_analysier.data_analysis import DocumentAnalysis
from src.document_analysier.data_ingestion import DocumentHandler

# Ensure project root is in sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)


# Path to the PDF you want to test
PDF_PATH = (
    "/home/aignishant/Documents/genaiproject/dp/document_portal/"
    "data/document_analysis/NIPS-2017-attention-is-all-you-need-Paper.pdf"
)


class DummyFile:
    def __init__(self, file_path):
        self.name = Path(file_path).name
        self.path = file_path  # Required by DocumentHandler.save_pdf
        self._file_path = file_path

    def getbuffer(self):
        with open(self._file_path, "rb") as f:
            return f.read()


def main():
    try:
        # ---------- STEP 1: DATA INGESTION ----------
        print("Starting PDF ingestion...")

        # Verify if file exists before proceeding
        if not os.path.exists(PDF_PATH):
            print(f"Error: Test file not found at {PDF_PATH}")
            return

        dummy_pdf = DummyFile(PDF_PATH)

        handler = DocumentHandler(session_id="test_ingestion_analysis")

        saved_path = handler.save_pdf(dummy_pdf)
        print(f"PDF saved at: {saved_path}")

        # Read PDF content
        pdf_text = handler.read_pdf(saved_path)
        print(f"PDF content extracted ({len(pdf_text)} chars).")

        # ---------- STEP 2: DATA ANALYSIS ----------
        print("Starting Document Analysis...")

        analyzer = DocumentAnalysis()  # Auto-detects config
        result = analyzer.analyze_document(document_text=pdf_text)

        print("Analysis Result:")
        print(result)

    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
