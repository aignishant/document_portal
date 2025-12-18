import os
from unittest.mock import MagicMock, patch

from src.document_analysier.data_analysis import DocumentAnalysis
from src.document_analysier.data_ingestion import DocumentHandler
from tests.base import BaseTestCase


class TestWorkflow(BaseTestCase):

    @patch("src.document_analysier.data_analysis.load_dotenv")
    @patch("src.document_analysier.data_analysis.ModelLoader")
    @patch("src.document_analysier.data_analysis.JsonOutputParser")
    @patch("src.document_analysier.data_analysis.OutputFixingParser")
    @patch("src.document_analysier.data_analysis.PROMPT_REGISTRY")
    def test_workflow_ingestion_and_analysis_success(
        self,
        mock_registry,
        mock_fixing_parser,
        mock_json_parser,
        mock_model_loader,
        mock_load_dotenv,
        temp_data_dir,
        sample_pdf,
        dummy_file_class,
    ):

        mock_llm = MagicMock()

        mock_model_loader.return_value.load_llm.return_value = mock_llm

        mock_prompt_template = MagicMock()

        mock_registry.__getitem__.return_value = mock_prompt_template

        mock_intermediate_chain = MagicMock()

        mock_final_chain = MagicMock()

        mock_prompt_template.__or__.return_value = mock_intermediate_chain

        mock_intermediate_chain.__or__.return_value = mock_final_chain

        expected_result = {
            "title": "Attention Is All You Need",
            "authors": ["Vaswani et al."],
            "summary": "Transformers are great.",
        }

        mock_final_chain.invoke.return_value = expected_result

        session_id = "test_workflow_session"

        handler = DocumentHandler(session_id=session_id)

        dummy_file = dummy_file_class(sample_pdf)

        saved_path = handler.save_pdf(dummy_file)

        assert os.path.exists(saved_path)

        assert session_id in saved_path

        pdf_text = handler.read_pdf(saved_path)

        assert len(pdf_text) > 0

        assert "Hello, World!" in pdf_text

        analyzer = DocumentAnalysis(config_path="dummy_path")

        result = analyzer.analyze_document(document_text=pdf_text)

        assert result == expected_result

        mock_final_chain.invoke.assert_called_once()

        assert "document_text" in mock_final_chain.invoke.call_args[0][0]
