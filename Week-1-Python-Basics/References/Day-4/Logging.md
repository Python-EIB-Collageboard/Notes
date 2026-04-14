# Logging

## Objective
Implementation of diagnostic telemetry, configurable log levels, and standardized application output tracking.

## JavaScript Equivalent
JavaScript developers typically use `console.log/warn/error` for superficial diagnostics. For production applications, JavaScript engineers must externalize this logic using robust third-party ecosystem libraries like Winston, Pino, or Bunyan.

## Implementation Details

### The Inadequacy of `print()`
In Python, using `print()` for production diagnostics is a recognized anti-pattern. `print()` writes synchronously to standard output, provides zero contextual metadata (like timestamps or module names), and cannot be filtered or efficiently routed to files. Python solves this via the built-in `logging` module.

### Core Architecture: Loggers, Handlers, and Formatters
The Python logging architecture relies on three distinct components:
1. **Loggers:** The entry point. Application code calls methods on a logger instance (e.g., `logger.info("message")`). Loggers are hierarchical and named, often mapping to the module path (`__name__`).
2. **Handlers:** Responsible for routing the log message to its final destination (e.g., `StreamHandler` for console, `FileHandler` for disk, `SysLogHandler` for networks).
3. **Formatters:** Responsible for converting the raw log event into a structured string or JSON byte stream.

### Log Levels
Messages are filtered based on severity. The standard hierarchy (lowest to highest) is:
- `DEBUG` (10): Granular detail for isolating bugs.
- `INFO` (20): Expected system events and state transitions.
- `WARNING` (30): Non-fatal anomalies that require attention. (Default threshold)
- `ERROR` (40): Operation failures that interrupt local execution flows.
- `CRITICAL` (50): Fatal state anomalies requiring application exit.

### Error Introspection
The `logging` module provides a specialized `logging.exception("message")` method. This method automatically captures the current exception context and appends a full stack trace to the log message. This is critical for post-mortem debugging.

## Code Comparison

**JavaScript (Node.js)**
```javascript
// Native limited execution
console.debug("Low level db trace");
console.info("Server listening on 3000");
console.warn("Deprecation notice");
console.error("Database connection refused");

// To match Python's native capability, JS requires:
// const winston = require('winston');
// const logger = winston.createLogger({ ... });
```

**Python**
```python
import logging

# Basic configuration (global settings for the root logger)
# Highly advised to configure this once at the application entry point
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler("system.log"),
        logging.StreamHandler()
    ]
)

# Standard practice: Instantiate a logger specific to the current module
logger = logging.getLogger(__name__)

def interface_database():
    logger.debug("Attempting to cycle connection pool.")
    logger.info("Database synchronized.")
    logger.warning("Query execution exceeded 500ms.")

def process_transaction(amount):
    try:
        if amount < 0:
            raise ValueError("Negative transaction unauthorized.")
    except ValueError:
        # Automatically logs ERROR level AND appends the stack trace
        logger.exception("Transaction processing failed.")

interface_database()
```

## Documentation
- [Python Standard Library: logging](https://docs.python.org/3/library/logging.html)
- [Python Logging HOWTO](https://docs.python.org/3/howto/logging.html)
