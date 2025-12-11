# Advanced Exception System Overview

This document provides a guide to using the custom exception handling system in the Document Portal.

## Overview

The system allows you to raise structured exceptions that carry specific error codes, HTTP status codes, and additional context. These exceptions automatically integrate with the project's advanced logger to ensure consistent JSON logging.

## Exception Classes

All exceptions inherit from `DocumentPortalException`.

| Exception Class | HTTP Status | Error Code | Usage |
|-----------------|-------------|------------|-------|
| `DocumentPortalException` | 500 | `INTERNAL_ERROR` | Base class, can be used for generic errors. |
| `ResourceNotFoundException` | 404 | `RESOURCE_NOT_FOUND` | When a requested resource (file, user, etc.) does not list. |
| `ValidationException` | 400 | `VALIDATION_ERROR` | When input data is invalid. |
| `AuthenticationException` | 401 | `AUTHENTICATION_FAILED` | When authentication fails or is missing. |
| `PermissionDeniedException` | 403 | `PERMISSION_DENIED` | When an authenticated user lacks access rights. |
| `DatabaseException` | 500 | `DATABASE_ERROR` | For database-related failures. |

## Usage Examples

### 1. Basic Usage

Raise a specific exception when an error condition is met.

```python
from exception.custom_exception import ResourceNotFoundException

def get_user(user_id):
    user = find_user_in_db(user_id)
    if not user:
        raise ResourceNotFoundException(f"User with ID {user_id} not found")
    return user
```

### 2. Adding Context Details

You can pass a dictionary of `details` to provide more context (e.g., specific invalid fields, query parameters).

```python
from exception.custom_exception import ValidationException

def create_document(data):
    if "title" not in data:
        raise ValidationException(
            "Missing required field 'title'",
            details={"field": "title", "input_data": data}
        )
```

### 3. Catching and Logging

You can use the `log_error()` method to automatically log the exception with all its structured data (code, status, details) using the application's JSON logger.

```python
from exception.custom_exception import DocumentPortalException
from flask import jsonify

@app.errorhandler(DocumentPortalException)
def handle_custom_exception(e):
    # Log the error with structured context
    e.log_error()
    
    # Return a consistent JSON response
    return jsonify(e.to_dict()), e.status_code
```

### 4. Custom Error Codes

If you need a specific error code for a unique situation, you can override it when raising the base exception (or subclass if applicable).

```python
raise DocumentPortalException(
    "External service timeout",
    code="EXTERNAL_SERVICE_TIMEOUT",
    status_code=503
)
```
