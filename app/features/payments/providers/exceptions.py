from app.core.app_exception import (
    AppException,
)


class PaymentProviderError(
    AppException
):
    status_code: int = 502
    log_level: str = "ERROR"
    error_code: str = (
        "payment_provider_error"
    )

    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        http_status: int | None = None,
        context: dict | None = None,
    ) -> None:
        provider_context = {
            "provider_code": code,
            "provider_http_status": (
                http_status
            ),
            **(context or {}),
        }

        super().__init__(
            message,
            provider_context,
        )

        self.code = code
        self.http_status = (
            http_status
        )

class PaymentDeclinedError(
    PaymentProviderError
):
    status_code: int = 402
    log_level: str = "WARNING"
    error_code: str = (
        "payment_declined"
    )

class UnsupportedPaymentStatusError(
    PaymentProviderError
):
    status_code: int = 502
    log_level: str = "ERROR"
    error_code: str = (
        "unsupported_payment_status"
    )