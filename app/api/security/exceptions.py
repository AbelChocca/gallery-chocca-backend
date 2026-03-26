from app.core.app_exception import AppException

class TooManyRequests(AppException):
    status_code: int = 429
    log_level: str = "WARNING"
    error_code: str = "too_many_requests_warning"

    def __init__(self, message, context: dict|None = None):
        super().__init__(message, context)

class SecurityException(AppException):
    status_code: int = 403
    log_level: str = "WARNING"
    error_code: str = "security_warning"

    def __init__(self, message, context: dict|None = None):
        super().__init__(message, context)

class AuthException(AppException):
    status_code: int = 401
    log_level: str = "WARNING"
    error_code: str = "auth_warning"

    def __init__(self, message, context: dict|None = None):
        super().__init__(message, context)