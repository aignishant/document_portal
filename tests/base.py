import json
import logging

from AIFoundationKit.base.logger.custom_logger import JsonFormatter, get_logger


class BaseTestCase:

    def setup_method(self, method):

        pass

    def teardown_method(self, method):

        pass

    def get_capture_logger(self, name="test_logger", level=logging.INFO):

        logger = get_logger(name)

        logger.handlers.clear()

        logger.setLevel(level)

        class ListHandler(logging.Handler):

            def __init__(self):

                super().__init__()

                self.records = []

            def emit(self, record):

                self.records.append(self.format(record))

        list_handler = ListHandler()

        list_handler.setFormatter(JsonFormatter())

        logger.addHandler(list_handler)

        return list_handler, logger

    def parse_log_record(self, log_json):

        return json.loads(log_json)
