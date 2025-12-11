import os
import sys

# Ensure the project root is in the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from exception.custom_exception import (
    ResourceNotFoundException,
    ValidationException,
    AuthenticationException,
    PermissionDeniedException,
    DatabaseException
)
from logger.custom_logger import logger

def mimic_business_logic(user_id: int):
    """Simulates a function that might raise various exceptions."""
    logger.info(f"Processing request for user_id={user_id}")
    
    if user_id < 0:
        raise ValidationException(
            "User ID cannot be negative",
            details={"user_id": user_id, "constraint": "must be positive"}
        )
    
    if user_id == 0:
        raise AuthenticationException("Anonymous access not allowed")
    
    if user_id == 99:
        raise PermissionDeniedException("User is banned")
        
    if user_id == 404:
        raise ResourceNotFoundException(f"User {user_id} does not exist")

    if user_id == 500:
        raise DatabaseException("Connection to database failed")
        
    logger.info(f"User {user_id} processed successfully")

def main():
    test_cases = [-1, 0, 99, 404, 500, 1]
    
    print("--- Starting Exception Usage Demo ---\n")
    
    for uid in test_cases:
        try:
            print(f"Testing user_id={uid}...")
            mimic_business_logic(uid)
        except (ValidationException, AuthenticationException, PermissionDeniedException, 
                ResourceNotFoundException, DatabaseException) as e:
            
            # Log the error using the built-in helper
            # This will write a structured JSON log entry
            e.log_error()
            
            # Print what would be sent to the API client
            print(f"Caught {e.__class__.__name__}:")
            print(f"  Status Code: {e.status_code}")
            print(f"  Response Body: {e.to_dict()}")
            print("-" * 40)
        except Exception as e:
            logger.exception("Unexpected error occurred")
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
