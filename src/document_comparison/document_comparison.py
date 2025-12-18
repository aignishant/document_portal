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
    def __init__(self):
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

    def compare_documents(self, doc1_text: str, doc2_text: str):
        try:
            combined_docs = f"Document 1:\n{doc1_text}\n\nDocument 2:\n{doc2_text}"
            response = self.chain.invoke(
                {
                    "combined_docs": combined_docs,
                    "format_instruction": self.output_parser.get_format_instructions(),
                }
            )
            self.logger.info("Documents compared successfully")
            return response
        except Exception as e:
            self.logger.error("Failed to compare documents: %s", e)
            raise AppException(f"Failed to compare documents: {str(e)}") from e

    def _format_response(self, response: dict) -> dict:
        try:
            return response
        except Exception as e:
            self.logger.error("Failed to format response: %s", e)
            raise AppException(f"Failed to format response: {str(e)}") from e


if __name__ == "__main__":
    document_comparison = DocumentComparisonWithLLM()
    doc1 = """
    Page 1:
    Project Alpha is expected to launch in Q3.
    Budget is set at $50,000.
    """
    doc2 = """
    Page 1:
    Project Alpha is expected to launch in Q4.
    Budget is set at $60,000.
    """
    result = document_comparison.compare_documents(doc1, doc2)
    print(result)

