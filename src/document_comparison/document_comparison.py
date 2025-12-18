import pandas as pd
from AIFoundationKit.base.exception.custom_exception import AppException
from AIFoundationKit.base.logger.custom_logger import get_logger
from AIFoundationKit.base.logger.logger_utils import add_context
from AIFoundationKit.base.utils import generate_session_id
from AIFoundationKit.rag.model_loader import ModelLoader
from dotenv import load_dotenv
from langchain_classic.output_parsers import OutputFixingParser
from langchain_core.output_parsers import JsonOutputParser

from model.models import SummaryResponse
from prompt.prompt_lib import PROMPT_REGISTRY


class DocumentComparisonWithLLM:
    """
    A class for comparing two documents using a Large Language Model (LLM).

    This class handles the initialization of the LLM, prompt templates,
    and output parsers required for structural comparison of document content.
    """

    def __init__(self):
        """
        Initializes the DocumentComparisonWithLLM class.

        Sets up the environment, logger, LLM loader, prompts, and output parsing chain.
        """

        load_dotenv()

        self.logger = get_logger(__name__)

        self.logger = add_context(self.logger, session_id=generate_session_id())

        self.model_loader = ModelLoader()

        self.llm = self.model_loader.load_llm()

        self.prompt = PROMPT_REGISTRY.get("document_comparison")

        self.output_parser = JsonOutputParser(pydantic_object=SummaryResponse)

        self.parser = OutputFixingParser.from_llm(
            llm=self.llm,
            parser=self.output_parser,
        )

        self.chain = self.prompt | self.llm | self.parser

        self.logger.info("Document comparison with LLM initialized successfully")

    def compare_documents(self, combined_docs: str):
        """
        Compares two provided document texts using the configured LLM chain.

        Args:
            doc1_text (str): The text content of the first document.
            doc2_text (str): The text content of the second document.

        Returns:
            dict: The structural comparison result from the LLM.

        Raises:
            AppException: If the comparison process fails.
        """

        try:

            response = self.chain.invoke(
                {
                    "combined_docs": combined_docs,
                    "format_instruction": self.output_parser.get_format_instructions(),
                }
            )

            self.logger.info("Documents compared successfully")

            return self._format_response(response)

        except Exception as e:

            self.logger.error("Failed to compare documents: %s", e)

            raise AppException(f"Failed to compare documents: {str(e)}") from e

    def _format_response(self, response: list[dict]) -> pd.DataFrame:
        """
        Formats the LLM response. Currently returns the response as is.

        Args:
            response (dict): The raw response dictionary from the LLM.

        Returns:
            dict: The formatted response dictionary.

        Raises:
            AppException: If formatting fails.
        """

        try:

            df = pd.DataFrame(response)

            self.logger.info("Response formatted successfully %s", df)

            return df

        except Exception as e:

            self.logger.error("Failed to format response: %s", e)

            raise AppException(f"Failed to format response: {str(e)}") from e


def main():
    """
    Main entry point for testing document comparison.
    """
    document_comparison = DocumentComparisonWithLLM()

    doc1 = """
    Project Alpha is expected to launch in Q3.
    Budget is set at $50,000.
    """

    doc2 = """
    Project Alpha is expected to launch in Q4.
    Budget is set at $60,000.
    """

    combined_docs = f"Document 1:\n{doc1}\n\nDocument 2:\n{doc2}"

    result = document_comparison.compare_documents(combined_docs)

    print(result)


if __name__ == "__main__":
    main()
