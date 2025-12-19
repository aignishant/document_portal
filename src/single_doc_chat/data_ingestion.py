import sys
from pathlib import Path

from AIFoundationKit.base.exception.custom_exception import AppException
from AIFoundationKit.base.logger.custom_logger import get_logger
from AIFoundationKit.base.logger.logger_utils import add_context
from AIFoundationKit.base.utils import generate_session_id
from AIFoundationKit.rag.model_loader import ModelLoader
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter


class SingleDocIngestor:
    def __init__(self):
        try:
            load_dotenv()
            self.logger = get_logger(__name__)
            self.logger = add_context(self.logger, session_id=generate_session_id())
            self.model_loader = ModelLoader()
            self.logger.info("Single document ingestor initialized successfully")
        except Exception as e:
            self.logger.error(
                "Failed to initialize single document ingestor: %s", str(e)
            )
            raise AppException(
                f"Failed to initialize single document ingestor: {str(e)}"
            ) from e

    def ingest_files(self, file_path: Path):
        try:
            pass
        except Exception as e:
            self.logger.error("Failed to ingest single document: %s", str(e))
            raise AppException(f"Failed to ingest single document: {str(e)}") from e

    def _create_retriever(self):
        try:
            pass
        except Exception as e:
            self.logger.error("Failed to create retriever: %s", str(e))
            raise AppException(f"Failed to create retriever: {str(e)}") from e
