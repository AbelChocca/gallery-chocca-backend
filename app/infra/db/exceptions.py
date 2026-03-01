from app.core.app_exception import AppException

class DatabaseException(AppException):
    status_code: int = 500
    log_level: str = "ERROR"
    error_code: str = "database_exception"

    def __init__(self, message: str, context: dict | None = None):
        super().__init__(message, context)