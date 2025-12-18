import os
from pathlib import Path
from typing import BinaryIO, Tuple, Union

from AIFoundationKit.base.exception.custom_exception import AppException
from AIFoundationKit.base.file_manager import BaseFileManager
from AIFoundationKit.base.logger.custom_logger import get_logger
from AIFoundationKit.base.logger.logger_utils import add_context
from AIFoundationKit.base.utils import generate_session_id

from src.constants import ERR_DOC_HANDLER_INIT


class DocumentComparisonHandler:
    """
    Handler for managing document comparison operations, including file storage
    and retrieval.
    """

    def __init__(
        self, session_id: str = None, file_path: str = "data/document_compare"
    ):
        """
        Initializes the DocumentComparisonHandler.

        Args:
            session_id (str, optional): Unique session identifier.
                                        Defaults to a generated ID.
            file_path (str, optional): Path to the directory where files will be stored.
                                        Defaults to 'data' directory in project root.
        """

        try:

            self.logger = get_logger(__name__)

            self.session_id = session_id or generate_session_id()

            self.logger.info(
                "Document comparison handler initialized with session ID: %s",
                self.session_id,
            )

            self.logger = add_context(self.logger, session_id=self.session_id)

            self.file_manager = BaseFileManager()

            project_root = Path(__file__).resolve().parent.parent.parent

            if file_path:
                path_obj = Path(file_path)
                if not path_obj.is_absolute():
                    base_dir = project_root / path_obj
                else:
                    base_dir = path_obj
            else:
                base_dir = project_root / "data"

            # Set file_path to the session directory
            self.file_path = base_dir / self.session_id
            self.file_path.mkdir(parents=True, exist_ok=True)

            self.logger.info(
                "Document comparison handler initialized with storage: %s",
                self.file_path,
            )

            self.logger.info("Document comparison handler initialized successfully")

        except Exception as e:

            self.logger.error("%s: %s", ERR_DOC_HANDLER_INIT, e)

            raise AppException(f"{ERR_DOC_HANDLER_INIT}: {str(e)}") from e

    def delete_existing_files(self):
        """
        Deletes all existing files in the configured file path directory.
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
        actual_file_name: str = None,
    ) -> Tuple[str, str]:
        """
        Saves the reference and actual files to the local storage.

        Args:
            reference_file (Union[str, BinaryIO, bytes]): The reference file content
                                                         or path.
            actual_file (Union[str, BinaryIO, bytes]): The actual file content or path.
            reference_file_name (str, optional): Name for the reference file.
            actual_file_name (str, optional): Name for the actual file.

        Returns:
            Tuple[str, str]: Paths where the reference and actual files were saved.
        """

        try:
            self.delete_existing_files()

            saved_ref_path = self._process_and_save(reference_file, reference_file_name)
            saved_act_path = self._process_and_save(actual_file, actual_file_name)

            self.logger.info("Saved files: %s, %s", saved_ref_path, saved_act_path)

            return saved_ref_path, saved_act_path

        except Exception as e:
            self.logger.error("Failed to save files: %s", e)
            raise AppException(f"Failed to save files: {str(e)}") from e

    def _process_and_save(
        self, file_input: Union[str, BinaryIO, bytes], file_name: str = None
    ) -> str:
        """
        Helper method to process and save a single file.

        Args:
            file_input (Union[str, BinaryIO, bytes]): The file content or path.
            file_name (str, optional): Name for the file.

        Returns:
            str: Path where the file was saved.
        """
        if isinstance(file_input, str):
            if not os.path.exists(file_input):
                raise FileNotFoundError(f"Source file not found: {file_input}")

            if not file_name:
                file_name = os.path.basename(file_input)

            with open(file_input, "rb") as f:
                file_content = f.read()

            saved_path = self.file_manager.save_file(
                file_content, str(self.file_path), file_name=file_name
            )
            return str(saved_path)

        saved_path = self.file_manager.save_file(
            file_input, str(self.file_path), file_name=file_name
        )
        return str(saved_path)

    def read_file(self, file_path: str) -> str:
        """
        Reads the content of a file.

        Args:
            file_path (str): The path to the file to be read.

        Returns:
            str: Content of the file.
        """

        try:

            return self.file_manager.read_file(file_path)

        except Exception as e:

            self.logger.error("Failed to read file %s: %s", file_path, e)

            raise AppException(f"Failed to read file {file_path}: {str(e)}") from e

    def combine_files(self) -> str:
        """
        Combines the reference and actual files into a single string.

        Returns:
            str: Combined content of the reference and actual files.
        """

        try:

            content_dict = {}
            doc_parts = []

            for file_path in sorted(self.file_path.iterdir()):

                if file_path.is_file():

                    file_name = file_path.name

                    file_content = self.read_file(str(file_path))

                    content_dict[file_name] = file_content

            for file_name, file_content in content_dict.items():

                doc_parts.append(f"{file_name}:\n{file_content}")

            combined_content = "\n\n".join(doc_parts)

            return combined_content

        except Exception as e:

            self.logger.error("Failed to combine files: %s", e)

            raise AppException(f"Failed to combine files: {str(e)}") from e

    def clean_old_session(self, keep_latest: int = 3):
        """
        Cleans up old sessions by removing all but the latest N sessions.

        Args:
            keep_latest (int, optional): Number of latest sessions to keep.
            Defaults to 3.
        """
        try:
            # self.file_path is the session folder,
            # so we check its parent for other sessions
            session_folders = sorted(
                [
                    folder
                    for folder in self.file_path.parent.iterdir()
                    if folder.is_dir()
                ],
                reverse=True,
            )
            for folder in session_folders[keep_latest:]:
                for file in folder.iterdir():
                    file.unlink()
                folder.rmdir()
                self.logger.info("Removed old session: %s", folder)
        except Exception as e:
            self.logger.error("Failed to clean old sessions: %s", e)
            raise AppException(f"Failed to clean old sessions: {str(e)}") from e


def main():
    """
    Main entry point for testing document handler.
    """
    try:
        handler = DocumentComparisonHandler()

        print("Initializing Document Comparison Handler...")

        # Test data
        ref_content = b"This is the reference document content."
        act_content = b"This is the actual document content."

        print("Saving files...")
        saved_paths = handler.save_file(
            reference_file=ref_content,
            actual_file=act_content,
            reference_file_name="reference.txt",
            actual_file_name="actual.txt",
        )
        print(f"Files saved at: {saved_paths}")

        print("Combining files...")
        combined = handler.combine_files()
        print("\nCombined Content Result:")
        print("-" * 20)
        print(combined)
        print("-" * 20)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
