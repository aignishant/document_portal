import pytest
import json
import logging
from ai_common.exception.custom_exception import (
    AppException,
    ResourceNotFoundException,
    ValidationException,
    AuthenticationException,
    PermissionDeniedException,
    DatabaseException
)
from ai_common.logger.custom_logger import JsonFormatter, get_logger

# Helper to capture logs
@pytest.fixture
def capture_logs():
    logger = get_logger('test_exception_logger')
    logger.handlers.clear()
    logger.setLevel(logging.ERROR)
    
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

def test_base_exception_initialization():
    exc = AppException(
        message="Something went wrong",
        code="TEST_ERROR",
        status_code=418,
        details={"foo": "bar"}
    )
    assert exc.message == "Something went wrong"
    assert exc.code == "TEST_ERROR"
    assert exc.status_code == 418
    assert exc.details == {"foo": "bar"}

def test_exception_to_dict():
    exc = AppException(
        message="Error",
        code="ERR",
        status_code=500
    )
    data = exc.to_dict()
    assert data["error"]["code"] == "ERR"
    assert data["error"]["message"] == "Error"
    assert data["error"]["details"] == {}

def test_exception_logging(capture_logs):
    handler, logger = capture_logs
    exc = AppException(
        message="Log me",
        code="LOG_ERR",
        status_code=500,
        details={"context": "test"}
    )
    exc.log_error(custom_logger=logger)
    
    assert len(handler.records) == 1
    log_json = json.loads(handler.records[0])
    
    assert log_json["message"] == "Log me"
    assert log_json["level"] == "ERROR"
    assert log_json["error_code"] == "LOG_ERR"
    assert log_json["status_code"] == 500
    assert log_json["error_details"] == {"context": "test"}

def test_subclasses_defaults():
    # ResourceNotFound
    exc = ResourceNotFoundException("Not found")
    assert exc.code == "RESOURCE_NOT_FOUND"
    assert exc.status_code == 404
    
    # Validation
    exc = ValidationException("Invalid input")
    assert exc.code == "VALIDATION_ERROR"
    assert exc.status_code == 400
    
    # Authentication
    exc = AuthenticationException("Who are you?")
    assert exc.code == "AUTHENTICATION_FAILED"
    assert exc.status_code == 401
    
    # PermissionDenied
    exc = PermissionDeniedException("Go away")
    assert exc.code == "PERMISSION_DENIED"
    assert exc.status_code == 403
    
    # Database
    exc = DatabaseException("DB Boom")
    assert exc.code == "DATABASE_ERROR"
    assert exc.status_code == 500
