import os
from pathlib import Path
from typing import BinaryIO, List, Union

from ai_common.exception.custom_exception import AppException
from ai_common.file_utils import read_any_file, save_uploaded_file
from ai_common.logger.custom_logger import get_logger
from ai_common.logger.logger_utils import add_context
from ai_common.utils import generate_session_id

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
            self.file_path = Path(file_path) if file_path else Path("data")
            self.file_path.mkdir(parents=True, exist_ok=True)
            self.logger.info("Document comparison handler initialized successfully")

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

    def save_uploaded_files(
        self, uploaded_files: List[Union[BinaryIO, bytes]]
    ) -> List[str]:
        """
        Saves uploaded files to the configured file path directory.

        Args:
            uploaded_files: List of file objects or bytes to save.

        Returns:
            List[str]: List of saved file absolute paths.
        """
        saved_paths = []
        try:
            for file_obj in uploaded_files:
                saved_file_path = save_uploaded_file(file_obj, str(self.file_path))
                saved_paths.append(saved_file_path)
            self.logger.info("Saved %s uploaded files", len(saved_paths))
            return saved_paths

        except Exception as e:
            self.logger.error("Failed to save uploaded files: %s", e)
            # Cleanup already saved files?? For now just raise
            raise AppException(f"Failed to save uploaded files: {str(e)}") from e

    def save_file(self, file_input: Union[str, BinaryIO, bytes], file_name: str = None) -> str:
        """
        Saves a single file to the managed directory.

        Args:
            file_input: File path (str), file object, or bytes.
            file_name: Optional file name. Required if valid name cannot be derived from input.

        Returns:
            str: Path to the saved file.
        """
        try:
            if isinstance(file_input, str):
                if not os.path.exists(file_input):
                    raise FileNotFoundError(f"Source file not found: {file_input}")

                # Derive name if not provided
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

            self.logger.info("Saved file: %s", saved_path)
            return saved_path

        except Exception as e:
            self.logger.error("Failed to save file: %s", e)
            raise AppException(f"Failed to save file: {str(e)}") from e

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


if __name__ == "__main__":
    import io

    # Mock file object
    class MockFile:
        def __init__(self, name, content):
            self.name = name
            self.content = content

        def read(self):
            return self.content

    handler = DocumentComparisonHandler(file_path="data/test_uploads")

    # Test text file
    txt_content = b"This is a test text file."
    txt_file = MockFile("test.txt", txt_content)

    # Test JSON file
    json_content = b'{"key": "value"}'
    json_file = MockFile("test.json", json_content)

    print("--- Saving Files ---")
    uploaded_file_paths = handler.save_uploaded_files([txt_file, json_file])
    print(f"Saved paths: {uploaded_file_paths}")

    print("\n--- Reading Files ---")
    for path in uploaded_file_paths:
        content = handler.read_file(path)
        print(f"File: {os.path.basename(path)}")
        print(f"Content: {content}")
        print("-" * 20)
