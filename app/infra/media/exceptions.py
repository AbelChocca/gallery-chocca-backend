from app.core.app_exception import AppException

class CloudinaryException(AppException):
    status_code: int = 500
    log_level: str = "ERROR"
    error_code: str = "cloudinary_error"

    def __init__(self, message: str, context: dict | None = None):
        super().__init__(message, context)