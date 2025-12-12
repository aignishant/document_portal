import os

import fitz
from ai_common.exception.custom_exception import AppException
from ai_common.logger.custom_logger import get_logger
from ai_common.logger.logger_utils import add_context
from ai_common.utils import generate_session_id

from src.constants import (
    DIR_DATA,
    DIR_DOCUMENT_ANALYSIS,
    ENV_DATA_STORAGE_PATH,
    ERR_DOC_HANDLER_INIT,
    ERR_INVALID_FILE_OBJ,
    ERR_PDF_NOT_FOUND,
    ERR_PDF_READ,
    ERR_PDF_SAVE,
    FITZ_TEXT_MODE,
    MSG_DOC_HANDLER_INIT,
    MSG_PDF_SAVED,
)


class DocumentHandler:
    """
    DocumentHandler class for handling document ingestion.

    This class manages the storage and retrieval of document files within a session context,
    ensuring documents are saved safely and can be read for downstream processing.
    """


    def __init__(self, data_dir: str = None, session_id: str = None) -> None:
        """
        Initializes the DocumentHandler instance.

        Args:
            data_dir (str, optional): The directory where data should be stored.
                Defaults to None, in which case a default 'data/document_analysis'
                directory is used.
            session_id (str, optional): A unique identifier for the session.
                Defaults to None, in which case a new session ID is generated.

        Raises:
            AppException: If initialization fails.
        """

        try:
            self.logger = get_logger(__name__)
            self.data_dir = data_dir or os.getenv(
                ENV_DATA_STORAGE_PATH,
                os.path.join(os.getcwd(), DIR_DATA, DIR_DOCUMENT_ANALYSIS),
            )
            self.session_id = session_id or generate_session_id()
            self.session_path = os.path.join(self.data_dir, self.session_id)
            if not os.path.exists(self.session_path):
                os.makedirs(self.session_path)

            self.logger = add_context(self.logger, session_id=self.session_id)
            self.logger.info(f"{MSG_DOC_HANDLER_INIT}: {self.session_id}")
        except Exception as e:
            self.logger.error(f"{ERR_DOC_HANDLER_INIT}: {str(e)}")
            raise AppException(f"{ERR_DOC_HANDLER_INIT}: {str(e)}")

    def save_pdf(self, file_obj) -> str:
        """
        Saves a PDF file-like object to the session directory.

        The method accepts an object with a ``path`` attribute (the source file
        path) and a ``getbuffer()`` method returning the file's bytes.

        Args:
            file_obj: A file-like object with `path` and `getbuffer()` attributes.

        Returns:
            str: The absolute path to the saved PDF file.

        Raises:
            AppException: If the file object is invalid or saving fails.
        """

        try:
            if not hasattr(file_obj, "path") or not hasattr(file_obj, "getbuffer"):
                raise AppException(ERR_INVALID_FILE_OBJ)

            if not os.path.exists(file_obj.path):
                raise AppException(f"{ERR_PDF_NOT_FOUND}: {file_obj.path}")

            pdf_name = os.path.basename(file_obj.path)
            dest_path = os.path.join(self.session_path, pdf_name)
            with open(dest_path, "wb") as f:
                f.write(file_obj.getbuffer())
            self.logger.info(f"{MSG_PDF_SAVED}: {dest_path}")
            return dest_path
        except Exception as e:
            self.logger.error(f"{ERR_PDF_SAVE}: {str(e)}")
            raise AppException(f"{ERR_PDF_SAVE}: {str(e)}")

    def read_pdf(self, pdf_path: str) -> list[str]:
        """
        Reads and extracts text from a PDF file.

        Args:
            pdf_path (str): The path to the PDF file to read.

        Returns:
            list[str]: A list of strings, where each string contains the text content
                of a page prefixed by its page number.
                Note: The current implementation returns a single string joined by newlines.
                (Signature annotation says list[str], implementation does join)

        Raises:
            AppException: If reading the PDF fails.
        """

        try:
            text_chunks = []
            with fitz.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf, start=1):
                    text = page.get_text(FITZ_TEXT_MODE)
                    text_chunks.append(f"\n--- Page {page_num}  ---\n{text}")
            text = "\n".join(text_chunks)
            return text
        except Exception as e:
            self.logger.error(f"{ERR_PDF_READ}: {str(e)}")
            raise AppException(f"{ERR_PDF_READ}: {str(e)}")


if __name__ == "__main__":
    from pathlib import Path


    document_handler = DocumentHandler(session_id="test_session")

    pdf_path = Path(
        "/home/aignishant/Documents/genaiproject/dp/document_portal/data/"
        "document_analysis/NIPS-2017-attention-is-all-you-need-Paper.pdf"
    )

    class DummyFile:
        def __init__(self, path):
            self.name = Path(path).name
            self.path = path

        def getbuffer(self):
            with open(self.path, "rb") as f:
                return f.read()

    try:
        document_handler.save_pdf(DummyFile(pdf_path))
        document_handler.logger.info(f"PDF saved to: {pdf_path}")
    except Exception as e:
        document_handler.logger.error(f"Failed to save PDF: {str(e)}")
        raise AppException(f"Failed to save PDF: {str(e)}")
    text = document_handler.read_pdf(pdf_path)
    document_handler.logger.info(f"PDF read from: {pdf_path}")
    document_handler.logger.info(f"PDF text: {text}")
