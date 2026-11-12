from app.core.app_exception import AppException

class ReceiptProviderError(AppException):
    status_code: int = 404
    log_level: str = "ERROR"
    error_code: str = "receipt_provider_error"

    def __init__(
        self,
        message: str = "Receipt Provider Error.",
        context: dict | None = None,
    ):
        super().__init__(message, context)

class ReceiptProviderInsufficientCredits(AppException):
    status_code: int = 402
    log_level: str = "WARNING"
    error_code: str = "receipt_provider_insufficient_credits"

    def __init__(
        self,
        message: str = "Insufficient receipt provider credits.",
        context: dict | None = None,
    ):
        super().__init__(message, context)


class ReceiptProviderInvalidRequest(AppException):
    status_code: int = 422
    log_level: str = "WARNING"
    error_code: str = "receipt_provider_invalid_request"

    def __init__(
        self,
        message: str,
        context: dict | None = None,
    ):
        super().__init__(message, context)