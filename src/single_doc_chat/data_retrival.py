import os
import sys
from pathlib import Path

from AIFoundationKit.base.exception.custom_exception import AppException
from AIFoundationKit.base.logger.custom_logger import get_logger
from AIFoundationKit.base.logger.logger_utils import add_context
from AIFoundationKit.base.utils import generate_session_id
from AIFoundationKit.rag.model_loader import ModelLoader
from dotenv import load_dotenv
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.history_aware_retriever import (
    create_history_aware_retriever,
)
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.vectorstores import FAISS
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from prompt.prompt_lib import PROMPT_REGISTRY
from src.utils import load_retriever_from_vectorstore


class ConversationlRAG:
    def __init__(self):
        try:
            load_dotenv()
            self.logger = get_logger(__name__)
            self.logger = add_context(self.logger, session_id=generate_session_id())
            self.logger.info("Conversation RAG initialized successfully")
        except Exception as e:
            self.logger.error("Failed to initialize conversation RAG: %s", str(e))
            raise AppException(
                f"Failed to initialize conversation RAG: {str(e)}"
            ) from e

    def _load_llm(self):
        try:
            self.logger.info("Loading LLM...")
            self.logger.info("LLM loaded successfully")
        except Exception as e:
            self.logger.error("Failed to load LLM: %s", str(e))
            raise AppException(f"Failed to load LLM: {str(e)}") from e

    def _get_session_history(self):
        try:
            self.logger.info("Getting session history...")
            self.logger.info("Session history retrieved successfully")
        except Exception as e:
            self.logger.error("Failed to get session history: %s", str(e))
            raise AppException(f"Failed to get session history: {str(e)}") from e

    def load_retriever_from_vectorstore(
        self, vectorstore, search_type="similarity", k=4
    ):
        try:
            self.logger.info("Loading retriever from vectorstore...")
            retriever = load_retriever_from_vectorstore(
                vectorstore, search_type=search_type, k=k)
            self.logger.info("Retriever loaded successfully")
            return retriever
        except Exception as e:
            self.logger.error("Failed to load retriever from vectorstore: %s", str(e))
            raise AppException(
                f"Failed to load retriever from vectorstore: {str(e)}"
            ) from e

    def invoke_retriever(self):
        try:
            self.logger.info("Invoking retriever...")
            self.logger.info("Retriever invoked successfully")
        except Exception as e:
            self.logger.error("Failed to invoke retriever: %s", str(e))
            raise AppException(f"Failed to invoke retriever: {str(e)}") from e
