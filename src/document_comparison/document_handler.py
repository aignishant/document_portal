import os
from pathlib import Path
from typing import BinaryIO, List, Tuple, Union

from rag_common.exception.custom_exception import AppException
from rag_common.file_utils import read_any_file, save_uploaded_file
from rag_common.logger.custom_logger import get_logger
from rag_common.logger.logger_utils import add_context
from rag_common.utils import generate_session_id

from src.constants import ERR_DOC_HANDLER_INIT


class DocumentComparisonHandler:
    """
    Handles document processing tasks for comparison.
    """

    def __init__(self, session_id: str = None, file_path: str = None):
        """
        Initialize the DocumentComparisonHandler.

        Args:
            session_id (str, optional): The session ID for logging. Defaults to generated ID.
            file_path (str, optional): The directory path to save/read files. Defaults to "data".
        """
        try:
            self.logger = get_logger(__name__)
            self.session_id = session_id or generate_session_id()
            self.logger = add_context(self.logger, session_id=self.session_id)

            # Determine project root (3 levels up: src/document_comparison/ -> src/ -> document_portal/)
            project_root = Path(__file__).resolve().parent.parent.parent

            if file_path:
                self.file_path = Path(file_path)
                if not self.file_path.is_absolute():
                    self.file_path = project_root / self.file_path
            else:
                self.file_path = project_root / "data"

            self.file_path.mkdir(parents=True, exist_ok=True)
            self.logger.info(
                f"Document comparison handler initialized with storage: {self.file_path}")
            self.logger.info("Document comparison handler initialized successfully")

        except Exception as e:
            self.logger.error("%s: %s", ERR_DOC_HANDLER_INIT, e)
            raise AppException(f"{ERR_DOC_HANDLER_INIT}: {str(e)}") from e

    def delete_existing_files(self):
        """
        Deletes the specified list of files from the filesystem.

        Args:
            file_paths (list[str]): A list of file paths to be deleted.
        """
        try:
            if self.file_path.exists() and self.file_path.is_dir():
                for file in self.file_path.iterdir():
                    if file.is_file():
                        file.unlink()
                        self.logger.info("Deleted file: %s", file)
                self.logger.info("Deleted existing files successfully")
            else:
                self.logger.info("No existing files found")
        except Exception as e:
            self.logger.error("Failed to delete existing files: %s", e)
            raise AppException(f"Failed to delete existing files: {str(e)}") from e

    def save_file(
        self,
        reference_file: Union[str, BinaryIO, bytes],
        actual_file: Union[str, BinaryIO, bytes],
        reference_file_name: str = None,
        actual_file_name: str = None
    ) -> Tuple[str, str]:
        """
        Saves both reference and actual files to the managed directory.

        Args:
            reference_file: Reference file path (str), file object, or bytes.
            actual_file: Actual file path (str), file object, or bytes.
            reference_file_name: Optional name for reference file.
            actual_file_name: Optional name for actual file.

        Returns:
            Tuple[str, str]: Tuple containing (reference_file_path, actual_file_path).
        """
        try:
            saved_paths = []
            self.delete_existing_files()

            for file_input, file_name in [(reference_file, reference_file_name), (actual_file, actual_file_name)]:
                if isinstance(file_input, str):
                    if not os.path.exists(file_input):
                        raise FileNotFoundError(f"Source file not found: {file_input}")

                    if not file_name:
                        file_name = os.path.basename(file_input)

                    with open(file_input, "rb") as f:
                        file_content = f.read()

                    saved_path = save_uploaded_file(
                        file_content, str(self.file_path), file_name=file_name)

                else:

                    saved_path = save_uploaded_file(
                        file_input, str(self.file_path), file_name=file_name
                    )
                saved_paths.append(saved_path)

            self.logger.info("Saved files: %s", saved_paths)
            return tuple(saved_paths)

        except Exception as e:
            self.logger.error("Failed to save files: %s", e)
            raise AppException(f"Failed to save files: {str(e)}") from e

    def read_file(self, file_path: str) -> str:
        """
        Reads content from the specified file path using generic file reader.

        Args:
            file_path (str): Path to the file to read.

        Returns:
            str: Extracted text content of the file.
        """
        try:
            return read_any_file(file_path)
        except Exception as e:
            self.logger.error("Failed to read file %s: %s", file_path, e)
            raise AppException(f"Failed to read file {file_path}: {str(e)}") from e
