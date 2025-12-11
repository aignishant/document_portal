import os

# Ensure log directory exists
os.makedirs('logs', exist_ok=True)

from ai_common.logger.custom_logger import logger
from ai_common.logger.logger_utils import add_context

# Create a logger with extra context
context_logger = add_context(logger, request_id='req-123', user_id='user-456')

context_logger.debug('Debug message with context')
context_logger.info('Info message with context')
context_logger.warning('Warning message')
context_logger.error('Error occurred')
context_logger.critical('Critical issue')

print('Logging complete. Check logs/app.log for entries.')
