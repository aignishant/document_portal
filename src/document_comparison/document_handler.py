import sys
import os
from dotenv import load_dotenv

import fitz
from src.constants import ERR_DOC_HANDLER_INIT
from ai_common.exception.custom_exception import AppException
from ai_common.logger.custom_logger import get_logger
from ai_common.logger.logger_utils import add_context
from ai_common.utils import generate_session_id


class DocumentHandler:
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

