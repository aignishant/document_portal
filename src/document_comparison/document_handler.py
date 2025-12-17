import sys
import os
from dotenv import load_dotenv

import fitz
from src.constants import ERR_DOC_HANDLER_INIT
from ai_common.exception.custom_exception import AppException
from ai_common.logger.custom_logger import get_logger
from ai_common.logger.logger_utils import add_context
from ai_common.utils import generate_session_id


class DocumentComparisonHandler:
    """
    Handles document processing tasks for comparison.
    """

    def __init__(self, session_id: str = None):
        try:
            self.logger = get_logger(__name__)
            self.session_id = session_id or generate_session_id()
            self.logger = add_context(self.logger, session_id=self.session_id)
        except Exception as e:
            self.logger.error("%s: %s", ERR_DOC_HANDLER_INIT, e)
            raise AppException(f"{ERR_DOC_HANDLER_INIT}: {str(e)}") from e

    def delete_existing_files(self, file_paths: list[str]):
        """
        Deletes the specified list of files from the filesystem.

        Args:
            file_paths (list[str]): A list of file paths to be deleted.
        """
        try:
            for file_path in file_paths:
                if os.path.exists(file_path):
                    os.remove(file_path)
            self.logger.info("Deleted existing files: %s", file_paths)
        except Exception as e:
            self.logger.error("Failed to delete existing files: %s", e)
            raise AppException(f"Failed to delete existing files: {str(e)}") from e

    def save_uploaded_files(self):
        try:
            pass
        except Exception as e:
            self.logger.error("Failed to save uploaded files: %s", e)
            raise AppException(f"Failed to save uploaded files: {str(e)}") from e

    def read_file(self):
        try:
            pass
        except Exception as e:
            self.logger.error("Failed to read files: %s", e)
            raise AppException(f"Failed to read files: {str(e)}") from e