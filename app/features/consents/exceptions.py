from app.core.app_exception import AppException

class TermsNotAcceptedError(AppException):
    status_code: int = 403
    log_level: str = "ERROR"
    error_code: str = "terms_not_accepted"

    def __init__(self, message: str, context: dict|None = None):
        super().__init__(message, context)

