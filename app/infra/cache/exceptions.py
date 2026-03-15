from app.core.app_exception import AppException

class InternalCacheException(AppException):
    status_code: int = 503
    log_level: str = "ERROR"
    error_code: str = "cache_internal_error"

    def __init__(self, message: str = "Cache Internal's error", context: dict | None = None):
        super().__init__(message, context)