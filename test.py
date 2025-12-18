# import os
# from pathlib import Path
# from src.document_analyzer.data_ingestion import DocumentHandler
# # Your PDFHandler class
# from src.document_analyzer.data_analysis import DocumentAnalyzer
# # Your DocumentAnalyzer class

# # Path to the PDF you want to test
# PDF_PATH = r"C:\\Users\\sunny\\document_portal\\data\\document_analysis\\sample.pdf"

# # Dummy file wrapper to simulate uploaded file (Streamlit style)
# class DummyFile:
#     def __init__(self, file_path):
#         self.name = Path(file_path).name
#         self._file_path = file_path

#     def getbuffer(self):
#         return open(self._file_path, "rb").read()

# def main():
#     try:
#         # ---------- STEP 1: DATA INGESTION ----------
#         print("Starting PDF ingestion...")
#         dummy_pdf = DummyFile(PDF_PATH)

#         handler = DocumentHandler(session_id="test_ingestion_analysis")

#         saved_path = handler.save_pdf(dummy_pdf)
#         print(f"PDF saved at: {saved_path}")

#         text_content = handler.read_pdf(saved_path)
#         print(f"Extracted text length: {len(text_content)} chars\n")

#         # ---------- STEP 2: DATA ANALYSIS ----------
#         print("Starting metadata analysis...")
#         analyzer = DocumentAnalyzer()  # Loads LLM + parser

#         analysis_result = analyzer.analyze_document(text_content)

#         # ---------- STEP 3: DISPLAY RESULTS ----------
#         print("\n=== METADATA ANALYSIS RESULT ===")
#         for key, value in analysis_result.items():
#             print(f"{key}: {value}")

#     except Exception as e:
#         print(f"Test failed: {e}")

# if __name__ == "__main__":
#     main()

import io
from pathlib import Path

from src.document_comparison.document_comparison import DocumentComparisonWithLLM
from src.document_comparison.document_handler import DocumentComparisonHandler


def load_fake_uploaded_file(file_path: Path):
    return io.BytesIO(file_path.read_bytes())


def test_compare_docuemnts():
    ref_path = Path(
        "/home/aignishant/Documents/genaiproject/dp/document_portal/Long_Report_V1.pdf"
    )
    act_path = Path(
        "/home/aignishant/Documents/genaiproject/dp/document_portal/Long_Report_V2.pdf"
    )

    class FakeUpload(io.BytesIO):
        def __init__(self, file_path: Path):
            self.name = file_path.name
            super().__init__(file_path.read_bytes())

    comparator = DocumentComparisonHandler()
    ref_upload = FakeUpload(ref_path)
    act_upload = FakeUpload(act_path)

    comparator.save_file(ref_upload, act_upload)
    combined_text = comparator.combine_files()
    comparator.clean_old_session(keep_latest=3)

    print("\n Combined Text Preview (First 1500 chars):\n")
    print(combined_text[:1500])

    llm_comparator = DocumentComparisonWithLLM()
    comparison_df = llm_comparator.compare_documents(combined_text)

    print("\n=== COMPARISON RESULT ===")
    print(comparison_df.head())


if __name__ == "__main__":
    test_compare_docuemnts()
