import logging
import os

from AIFoundationKit.base.logger.logger_utils import add_context

from tests.base import BaseTestCase


class TestCustomLogger(BaseTestCase):

    def test_logger_output(self):

        os.environ["LOG_LEVEL"] = "DEBUG"

        list_handler, logger = self.get_capture_logger(
            name="test_logger", level=logging.DEBUG
        )

        context_logger = add_context(logger, test_key="test_value")

        context_logger.info("Test log message")

        for h in logger.handlers:

            h.flush()

        assert (
            len(list_handler.records) == 1
        ), f"Expected 1 log record, got {len(list_handler.records)}"

        log_record = self.parse_log_record(list_handler.records[0])

        assert log_record["message"] == "Test log message"

        assert log_record["level"] == "INFO"

        assert log_record.get("test_key") == "test_value"
