# universal_integer_system/src/transports/logging_config.py
"""Logging configuration for Universal Integer System."""

import logging
import sys
from typing import Any, Dict

import structlog
from pythonjsonlogger import jsonlogger

# Use standard logging for the root logger configuration
stdlib_logger = logging.getLogger("stdlib")
stdlib_logger.setLevel(logging.INFO)


def setup_logging(level: str = "INFO", enable_loki: bool = True) -> None:
    """Configure structured logging with optional Loki support.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        enable_loki: Whether to format logs for Loki ingestion
    """
    # Configure standard logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, level.upper()),
        force=True,  # Force reconfiguration if already configured
    )

    if enable_loki:
        # Configure JSON formatter for Loki
        log_handler = logging.StreamHandler(sys.stdout)
        formatter = jsonlogger.JsonFormatter(
            fmt="%(timestamp)s %(level)s %(name)s %(message)s",
            rename_fields={"timestamp": "time", "level": "severity"},
        )
        log_handler.setFormatter(formatter)

        # Clear existing handlers and add our JSON handler
        stdlib_logger.handlers.clear()
        stdlib_logger.addHandler(log_handler)

    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            add_app_context,  # Custom processor
            structlog.processors.JSONRenderer() if enable_loki else structlog.dev.ConsoleRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def add_app_context(
        logger: logging.Logger, method_name: str, event_dict: Dict[str, Any]
) -> Dict[str, Any]:
    """Add application context to all log entries.

    Args:
        logger: The logger instance
        method_name: The name of the method being called
        event_dict: The event dictionary to augment

    Returns:
        The augmented event dictionary
    """
    event_dict["app"] = "universal-integer-system"
    event_dict["version"] = "1.0.0"

    # Add trace ID if available in the context
    context = getattr(logger, "_context", {})
    if isinstance(context, dict) and "trace_id" in context:
        event_dict["trace_id"] = context["trace_id"]

    return event_dict


def get_logger(name: str = None) -> structlog.stdlib.BoundLogger:
    """Get a configured logger instance.

    Args:
        name: Logger name (typically __name__)

    Returns:
        A configured structlog logger
    """
    return structlog.get_logger(name)


# Example usage and testing
if __name__ == "__main__":
    # Setup logging
    setup_logging(level="DEBUG", enable_loki=False)

    # Get a logger
    logger = get_logger(__name__)

    # Test various log levels
    logger.debug("Debug message", extra_field="debug_value")
    logger.info("Info message", code=1001, system="auth")
    logger.warning("Warning message", threshold_exceeded=True)
    logger.error("Error message", error_code=500, details={"reason": "test error"})

    # Test with trace ID
    logger = logger.bind(trace_id="abc-123-def")
    logger.info("Message with trace ID", operation="test")