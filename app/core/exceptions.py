from app.core.app_exception import AppException

class ValidationError(AppException):
    status_code: int = 400
    log_level: str = "WARNING"
    error_code: str = "validation_error"

    def __init__(self, message: str, context: dict|None = None):
        super().__init__(message, context)

class ValueNotFound(AppException):
    status_code: int = 404
    log_level: str = "WARNING"
    error_code: str = "value_not_found_error"

    def __init__(self, message: str, context: dict|None = None):
        super().__init__(message, context)