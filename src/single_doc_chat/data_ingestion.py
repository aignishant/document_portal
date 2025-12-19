import os
from pathlib import Path

from AIFoundationKit.base.exception.custom_exception import AppException
from AIFoundationKit.base.logger.custom_logger import get_logger
from AIFoundationKit.base.logger.logger_utils import add_context
from AIFoundationKit.base.utils import generate_session_id
from AIFoundationKit.rag.model_loader import ModelLoader
from dotenv import load_dotenv
from langchain_core.documents import Document

from src.utils import ensure_directory_exists, process_and_load_files, _create_retriever


class SingleDocIngestor:
    def __init__(
        self,
        data_dir: str = "data/single_document_chat",
        faiss_dir: str = "data/faiss_index",
        session_id: str = None,
    ):
        try:
            load_dotenv()
            self.data_dir = ensure_directory_exists(data_dir)
            self.faiss_dir = ensure_directory_exists(faiss_dir)

            self.logger = get_logger(__name__)
            if session_id is None:
                self.logger = add_context(self.logger, session_id=generate_session_id())
            else:
                self.logger = add_context(self.logger, session_id=session_id)
            self.model_loader = ModelLoader()
            self.logger.info("Single document ingestor initialized successfully")
        except Exception as e:
            self.logger.error(
                "Failed to initialize single document ingestor: %s", str(e)
            )
            raise AppException(
                f"Failed to initialize single document ingestor: {str(e)}"
            ) from e

    def ingest_files(self, file_paths: list[str]) -> list[Document]:
        try:
            files = process_and_load_files(file_paths, self.data_dir)
            for file_path in file_paths:
                self.logger.info("Ingesting file: %s", file_path)

            embedding_model = self.model_loader.load_embeddings()
            return _create_retriever(
                files,
                embedding_model,
                self.faiss_dir
            )

        except Exception as e:
            self.logger.error("Failed to ingest single document: %s", str(e))
            raise AppException(f"Failed to ingest single document: {str(e)}") from e
