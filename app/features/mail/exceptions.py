from app.core.app_exception import AppException


class MailProviderError(AppException):
    status_code = 502
    log_level = "ERROR"
    error_code = "mail_provider_error"

    def __init__(
        self,
        message: str,
        context: dict | None = None,
    ) -> None:
        super().__init__(
            message,
            context,
        )