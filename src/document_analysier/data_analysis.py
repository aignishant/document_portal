import os
from ai_common.logger.custom_logger import logger, get_logger
from ai_common.logger.logger_utils import add_context
from ai_common.exception.custom_exception import AppException
from ai_common.model_loader import ModelLoader
from model.models import *
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser

class DocumentAnalysis:
    """
    DocumentAnalysis class for handling document analysis
    """
    def __init__(self):
        self.logger = get_logger(__name__)
        self.logger = add_context(self.logger, "DocumentAnalysis")
        self.logger.info("DocumentAnalysis initialized")
    
    def analyze_metadata(self):
        pass