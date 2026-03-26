from enum import Enum

class LogLevel(str, Enum):
    error = "ERROR"
    exception = "EXCEPTION"
    warning = "WARNING"
    info = "INFO"
    debug = "DEBUG"

class AppException(Exception):
    status_code: int = 500
    log_level: LogLevel = "ERROR"
    error_code: str = "internal_error"

    def __init__(self, message: str, context: dict | None = None):
        super().__init__(message)
        self.message = message
        self.context = context or {}

def serialize_exception(e: Exception):
    if isinstance(e, AppException):
        return {
            "type": type(e).__name__,
            "message": e.message,
            "context": e.context
        }
    return {
        "type": type(e).__name__,
        "message": str(e)
    }