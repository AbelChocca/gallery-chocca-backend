from app.core.app_exception import AppException

class JWTException(AppException):
    status_code: int = 401
    log_level: str = "ERROR"
    error_code: str = "jwt_error"

    def __init__(self, message: str, context: dict | None = None):
        super().__init__(message)
        self.message = message
        self.context = context or {}