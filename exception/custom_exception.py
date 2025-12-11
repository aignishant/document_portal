from typing import Optional, Dict, Any
from logger.custom_logger import logger
from logger.logger_utils import add_context

class DocumentPortalException(Exception):
    """Base exception for Document Portal."""
    
    def __init__(
        self, 
        message: str, 
        code: str = "INTERNAL_ERROR", 
        status_code: int = 500, 
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        
    def to_dict(self) -> Dict[str, Any]:
        """Serialize exception to dictionary."""
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details,
            }
        }

    def log_error(self, custom_logger=None):
        """Log the exception details with context."""
        log = custom_logger or logger
        context_data = {
            "error_code": self.code,
            "status_code": self.status_code,
            "error_details": self.details
        }
        ctx_logger = add_context(log, **context_data)
        ctx_logger.error(self.message)

class ResourceNotFoundException(DocumentPortalException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message, 
            code="RESOURCE_NOT_FOUND", 
            status_code=404, 
            details=details
        )

class ValidationException(DocumentPortalException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message, 
            code="VALIDATION_ERROR", 
            status_code=400, 
            details=details
        )

class AuthenticationException(DocumentPortalException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message, 
            code="AUTHENTICATION_FAILED", 
            status_code=401, 
            details=details
        )

class PermissionDeniedException(DocumentPortalException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message, 
            code="PERMISSION_DENIED", 
            status_code=403, 
            details=details
        )

class DatabaseException(DocumentPortalException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message, 
            code="DATABASE_ERROR", 
            status_code=500, 
            details=details
        )
