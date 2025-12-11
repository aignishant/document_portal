import os
import fitz
import uuid
from datetime import datetime

from ai_common.logger.custom_logger import logger, get_logger
from ai_common.logger.logger_utils import add_context
from ai_common.exception.custom_exception import AppException


class DocumentHandler:
    """
    DocumentHandler class for handling document ingestion
    """
    def __init__(self):
        self.logger = get_logger(__name__)
        self.logger = add_context(self.logger, "DocumentHandler")
        self.logger.info("DocumentHandler initialized")
    
    def save_pdf(self):
        pass

    def read_pdf(self):
        pass