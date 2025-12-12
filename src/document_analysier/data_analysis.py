import os
import sys

from ai_common.exception.custom_exception import AppException
from ai_common.logger.custom_logger import get_logger
from ai_common.logger.logger_utils import add_context
from ai_common.model_loader import ModelLoader
from dotenv import load_dotenv
from langchain_classic.output_parsers import OutputFixingParser
from langchain_core.output_parsers import JsonOutputParser
from prompt.prompt_lib import *
from model.models import Metadata
from src.constants import (
    COMPONENT_DOCUMENT_ANALYSIS,
    CONFIG_DIR,
    CONFIG_FILE,
    ERR_DOC_ANALYSIS_INIT,
    MSG_DOC_ANALYSIS_INIT,
)


class DocumentAnalysis:
    """
    DocumentAnalysis class for handling document analysis.

    This class initializes the document analysis component, loading configurations,
    models, and setting up the LLM for processing documents.
    """

    def __init__(self, config_path: str = None, prompt: str = None):
        """
        Initializes the DocumentAnalysis instance.

        Args:
            config_path (str, optional): Path to the configuration file or directory.
                Defaults to None, in which case it attempts to locate the config
                directory relative to the source tree.

        Raises:
            AppException: If initialization fails.
        """

        try:
            load_dotenv()
            self.logger = get_logger(__name__)
            self.logger = add_context(
                self.logger, component=COMPONENT_DOCUMENT_ANALYSIS
            )

            if config_path is None:
                current_dir = os.path.dirname(os.path.abspath(__file__))

                project_root = os.path.dirname(os.path.dirname(current_dir))

                config_path = os.path.join(project_root, CONFIG_DIR)

            if os.path.isdir(config_path):

                config_path = os.path.join(config_path, CONFIG_FILE)

            self.loader = ModelLoader(config_path=config_path)
            self.llm = self.loader.load_llm()

            self.parser = JsonOutputParser(pydantic_object=Metadata)
            self.fixing_parser = OutputFixingParser.from_llm(
                parser=self.parser, llm=self.llm
            )
            self.document_analysis_prompt = prompt if prompt else document_analysis_prompt

            self.logger.info(MSG_DOC_ANALYSIS_INIT)
        except Exception as e:
            self.logger.error("%s: %s", ERR_DOC_ANALYSIS_INIT, str(e))
            raise AppException(f"{ERR_DOC_ANALYSIS_INIT}:", sys) from e

    def analyze_document(self, document_text: str) -> dict:
        """
        Analyzes a document.

        This method is currently a placeholder for the document analysis logic.
        """
        self.logger.info('Document analysis started')
        try:
            chain = self.document_analysis_prompt | self.llm | self.fixing_parser
            self.logger.info("Document analysis completed successfully")
            response = chain.invoke({
                "format_instructions": self.parser.get_format_instructions(),
                "document_text": document_text
            })
            return response
        except Exception as e:
            self.logger.error("Document analysis failed: %s", str(e))
            raise AppException(f"Document analysis failed: {str(e)}") from e


if __name__ == "__main__":
    document_analysis = DocumentAnalysis()
    res = document_analysis.analyze_document(document_text="")
    print(res)
