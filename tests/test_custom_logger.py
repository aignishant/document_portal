import json
import logging
import logging.handlers
import os

# import pytest
from AIFoundationKit.base.logger.custom_logger import JsonFormatter, get_logger
from AIFoundationKit.base.logger.logger_utils import add_context


def test_logger_output():
    # Configure test environment
    os.environ["LOG_LEVEL"] = "DEBUG"
    # Initialize a fresh logger with a unique name for isolation
    logger = get_logger("test_logger")
    # Ensure no previous handlers interfere
    logger.handlers.clear()
    logger.setLevel("DEBUG")

    # In‑memory handler to capture log output for verification
    class ListHandler(logging.Handler):
        def __init__(self):
            super().__init__()
            self.records = []

        def emit(self, record):
            self.records.append(self.format(record))

    list_handler = ListHandler()
    list_handler.setFormatter(JsonFormatter())
    logger.addHandler(list_handler)

    # Add a console handler (optional, not used in assertions)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.addHandler(console_handler)

    # Create a logger with extra context using the adapter
    context_logger = add_context(logger, test_key="test_value")

    # Emit a log record
    context_logger.info("Test log message")

    # Flush handlers to ensure all records are processed
    for h in logger.handlers:
        h.flush()

    # Verify that the in‑memory handler captured exactly one record
    assert (
        len(list_handler.records) == 1
    ), f"Expected 1 log record, got {len(list_handler.records)}"
    log_json = list_handler.records[0]
    log_record = json.loads(log_json)
    assert log_record["message"] == "Test log message"
    assert log_record["level"] == "INFO"
    assert log_record.get("test_key") == "test_value"
