import os

import fitz
from AIFoundationKit.base.exception.custom_exception import AppException
from AIFoundationKit.base.logger.custom_logger import get_logger
from AIFoundationKit.base.logger.logger_utils import add_context
from AIFoundationKit.base.utils import generate_session_id

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

    def __init__(self, data_dir: str = None, session_id: str = None) -> None:

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
