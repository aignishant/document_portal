import os
import sys
from dotenv import load_dotenv

from ai_common.exception.custom_exception import AppException
from ai_common.logger.custom_logger import get_logger
from ai_common.logger.logger_utils import add_context
from ai_common.model_loader import ModelLoader
from langchain_classic.output_parsers import OutputFixingParser
from langchain_core.output_parsers import JsonOutputParser
from prompt.prompt_lib import PROMPT_REGISTRY
from model.models import Metadata
from ai_common.utils import generate_session_id


class DocumentComparisonWithLLM:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.logger = add_context(self.logger, session_id=generate_session_id())
        self.model_loader = ModelLoader()

    def compare_documents(self):
        try:
            pass
        except Exception as e:
            self.logger.error("Failed to compare documents: %s", e)
            raise AppException(f"Failed to compare documents: {str(e)}") from e

    def _format_response(self, response: dict) -> dict:
        try:
            pass
        except Exception as e:
            self.logger.error("Failed to format response: %s", e)
            raise AppException(f"Failed to format response: {str(e)}") from e
