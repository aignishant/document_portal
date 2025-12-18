import logging

from AIFoundationKit.base.exception.custom_exception import (
    AppException,
    AuthenticationException,
    DatabaseException,
    PermissionDeniedException,
    ResourceNotFoundException,
    ValidationException,
)

from tests.base import BaseTestCase


class TestCustomException(BaseTestCase):

    def test_base_exception_initialization(self):

        exc = AppException(
            message="Something went wrong",
            code="TEST_ERROR",
            status_code=418,
            details={"foo": "bar"},
        )

        assert exc.message == "Something went wrong"

        assert exc.code == "TEST_ERROR"

        assert exc.status_code == 418

        assert exc.details == {"foo": "bar"}

    def test_exception_to_dict(self):

        exc = AppException(message="Error", code="ERR", status_code=500)

        data = exc.to_dict()

        assert data["error"]["code"] == "ERR"

        assert data["error"]["message"] == "Error"

        assert data["error"]["details"] == {}

    def test_exception_logging(self):

        handler, logger = self.get_capture_logger(
            name="test_exception_logger", level=logging.ERROR
        )

        exc = AppException(
            message="Log me",
            code="LOG_ERR",
            status_code=500,
            details={"context": "test"},
        )

        exc.log_error(custom_logger=logger)

        assert len(handler.records) == 1

        log_record = self.parse_log_record(handler.records[0])

        assert log_record["message"] == "Log me"

        assert log_record["level"] == "ERROR"

        assert log_record["error_code"] == "LOG_ERR"

        assert log_record["status_code"] == 500

        assert log_record["error_details"] == {"context": "test"}

    def test_subclasses_defaults(self):

        exc = ResourceNotFoundException("Not found")

        assert exc.code == "RESOURCE_NOT_FOUND"

        assert exc.status_code == 404

        exc = ValidationException("Invalid input")

        assert exc.code == "VALIDATION_ERROR"

        assert exc.status_code == 400

        exc = AuthenticationException("Who are you?")

        assert exc.code == "AUTHENTICATION_FAILED"

        assert exc.status_code == 401

        exc = PermissionDeniedException("Go away")

        assert exc.code == "PERMISSION_DENIED"

        assert exc.status_code == 403

        exc = DatabaseException("DB Boom")

        assert exc.code == "DATABASE_ERROR"

        assert exc.status_code == 500
