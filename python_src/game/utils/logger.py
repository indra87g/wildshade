from loguru import logger
import sys

log_file = "wildshade.log"

logger.remove()
logger.add(
    log_file,
    rotation="1 MB",
    retention="5 days",
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="DEBUG",
)


def log_debug(message: str) -> None:
    """Logging for debugging."""
    logger.debug(message)


def log_info(message: str) -> None:
    """Logging for common information."""
    logger.info(message)


def log_warning(message: str) -> None:
    """Logger for warning."""
    logger.warning(message)


def log_error(message: str) -> None:
    """Logger for error."""
    logger.error(message)


def log_exception(message: str) -> None:
    """Logger for exception (use on `except`)."""
    logger.exception(message)


def exception_handler(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.error("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = exception_handler
