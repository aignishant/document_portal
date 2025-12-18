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

    def __init__(self, session_id: str = None, file_path: str = None):

        try:

            self.logger = get_logger(__name__)

            self.session_id = session_id or generate_session_id()

            self.logger = add_context(self.logger, session_id=self.session_id)

            self.file_manager = BaseFileManager()

            project_root = Path(__file__).resolve().parent.parent.parent

            if file_path:

                self.file_path = Path(file_path)

                if not self.file_path.is_absolute():

                    self.file_path = project_root / self.file_path

            else:

                self.file_path = project_root / "data"

            self.file_path.mkdir(parents=True, exist_ok=True)

            self.logger.info(
                f"Document comparison handler initialized with storage: "
                f"{self.file_path}"
            )

            self.logger.info("Document comparison handler initialized successfully")

        except Exception as e:

            self.logger.error("%s: %s", ERR_DOC_HANDLER_INIT, e)

            raise AppException(f"{ERR_DOC_HANDLER_INIT}: {str(e)}") from e

    def delete_existing_files(self):

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

        try:

            saved_paths = []

            self.delete_existing_files()

            for file_input, file_name in [
                (reference_file, reference_file_name),
                (actual_file, actual_file_name),
            ]:

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

                else:

                    saved_path = self.file_manager.save_file(
                        file_input, str(self.file_path), file_name=file_name
                    )

                saved_paths.append(saved_path)

            self.logger.info("Saved files: %s", saved_paths)

            return tuple(saved_paths)

        except Exception as e:

            self.logger.error("Failed to save files: %s", e)

            raise AppException(f"Failed to save files: {str(e)}") from e

    def read_file(self, file_path: str) -> str:

        try:

            return self.file_manager.read_file(file_path)

        except Exception as e:

            self.logger.error("Failed to read file %s: %s", file_path, e)

            raise AppException(f"Failed to read file {file_path}: {str(e)}") from e
