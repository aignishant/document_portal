# Advanced Logger Overview

This document provides a quick reference for the advanced logger implemented in this project.

## Files

| File | Description | Usage |
|------|-------------|-------|
| `logger/custom_logger.py` | Core logger implementation with JSON formatting and a rotating file handler. | `from logger.custom_logger import get_logger, logger` |
| `logger/logger_utils.py` | Helper utilities for adding contextual information via `ContextAdapter`. | `from logger.logger_utils import add_context` |
| `logger/example_usage.py` | Example script demonstrating typical usage. | Run the script to see logs in console and file. |
| `tests/test_custom_logger.py` | Pytest suite that verifies JSON output and extra fields. | `./myvenv/bin/pytest -q` |

## How to Use
```python
import os
from logger.custom_logger import logger          # module‑level logger
from logger.logger_utils import add_context

# Optional: override defaults for this run
os.environ['LOG_DIR'] = 'my_logs'
os.environ['LOG_LEVEL'] = 'DEBUG'

# Add custom context (e.g., request ID, user ID)
ctx_logger = add_context(logger, request_id='req-123', user_id='user-456')

ctx_logger.info('User logged in')
```

- Logs are written to `<LOG_DIR>/app.log` as JSON and rotated automatically.
- The console also receives plain‑text logs.
- Extra fields added via `add_context` appear as top‑level keys in the JSON output.

## Testing
Run the test suite with:
```bash
./myvenv/bin/pytest -q
```
The test creates an in‑memory handler to capture logs and asserts that the JSON contains the expected fields.

---
*Generated on 2025‑12‑11.*
