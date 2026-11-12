import httpx
from datetime import datetime

from app.features.payments.providers.base_provider import (
    BasePaymentProvider,
)
from app.features.payments.types.payment_provider import (
    CheckoutResult,
    CreateCheckoutRequest,
    CheckoutStatus,
    CreateCardChargeRequest,
    CardChargeResult
)

from app.core.settings.pydantic_settings import settings

from app.features.payments.providers.exceptions import (
    PaymentDeclinedError,
    PaymentProviderError,
    UnsupportedPaymentStatusError,
)

class OpenpayPaymentProvider(BasePaymentProvider):

    def __init__(
        self,
        client: httpx.AsyncClient,
    ) -> None:
        self._client = client

    async def create_card_charge(
        self,
        request: CreateCardChargeRequest,
    ) -> CardChargeResult:

        payload = {
            "source_id": request.token_id,
            "method": "card",
            "amount": round(float(request.amount), 2),
            "currency": request.currency,
            "description": request.description,
            "order_id": request.order_id,
            "device_session_id": (
                request.device_session_id
            ),
            "customer": {
                "name": request.customer.name,
                "last_name": (
                    request.customer.last_name
                ),
                "phone_number": (
                    request.customer.phone_number
                ),
                "email": request.customer.email,
            },
        }

        if request.use_3d_secure:
            payload["use_3d_secure"] = True

            if request.redirect_url:
                payload["redirect_url"] = (
                    request.redirect_url
                )

        base_url = settings.OPENPAY_BASE_URL.rstrip("/")

        url = (
            f"{base_url}"
            f"/v1/{settings.OPENPAY_MERCHANT_ID}/charges"
        )

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=payload,
                auth=(
                    settings.OPENPAY_PRIVATE_KEY,
                    "",
                ),
                headers={
                    "Content-Type":
                        "application/json",

                    "X-Forwarded-For":
                        request.client_ip,
                },
            )

        data = response.json()

        if response.status_code == 402:
            raise PaymentDeclinedError(
                message=(
                    "No pudimos autorizar el pago. "
                    "Intenta nuevamente o usa otra tarjeta."
                ),
                code=str(
                    data.get("error_code")
                ),
                http_status=(
                    response.status_code
                ),
                context={
                    "provider_message": (
                        data.get("description")
                    ),
                },
            )

        if response.is_error:
            raise PaymentProviderError(
                message=data.get(
                    "description",
                    "Openpay no pudo procesar el pago.",
                ),
                code=data.get(
                    "error_code",
                ),
            )

        response.raise_for_status()

        payment_method = (
            data.get("payment_method")
            or {}
        )

        return CardChargeResult(
            provider_payment_id=data["id"],
            status=data["status"],
            authorization=data.get(
                "authorization"
            ),
            error_message=data.get(
                "error_message"
            ),
            redirect_url=(
                payment_method.get("url")
            ),
        )

    async def create_checkout(
        self,
        request: CreateCheckoutRequest,
    ) -> CheckoutResult:
        response = await self._client.post(
            url=self._build_url("/checkouts"),
            json=self._build_checkout_payload(
                request
            ),
            auth=httpx.BasicAuth(
                username=settings.OPENPAY_PRIVATE_KEY,
                password="",
            ),
            timeout=15.0,
        )

        if response.is_error:
            self._raise_openpay_error(
                response
            )

        data = response.json()

        return CheckoutResult(
            provider_checkout_id=data["id"],

            status=self._map_checkout_status(
                data["status"]
            ),

            checkout_link=data[
                "checkout_link"
            ],

            creation_date=self._parse_openpay_datetime(
                data["creation_date"]
            ),

            expiration_date=(
                self._parse_openpay_datetime(
                    data["expiration_date"]
                )
                if data.get(
                    "expiration_date"
                )
                else None
            ),
        )
    
    @staticmethod
    def _build_url(path: str) -> str:
        base_url = settings.OPENPAY_BASE_URL.rstrip("/")

        return (
            f"{base_url}/v1/"
            f"{settings.OPENPAY_MERCHANT_ID}"
            f"{path}"
        )

    @staticmethod
    def _build_checkout_payload(
        request: CreateCheckoutRequest,
    ) -> dict:
        payload = {
            "amount": str(
                request.amount
            ),
            "currency": request.currency,

            "description": (
                request.description
            ),

            "order_id": request.order_id,

            "redirect_url": (
                request.redirect_url
            ),

            "send_email": (
                request.send_email
            ),

            "customer": {
                "name": (
                    request.customer.name
                ),

                "last_name": (
                    request.customer.last_name
                ),

                "email": (
                    request.customer.email
                ),

                "phone_number": (
                    request.customer.phone_number
                ),
            },
        }

        if (
            request.expiration_date
            is not None
        ):
            payload["expiration_date"] = (
                request.expiration_date.isoformat()
            )

        return payload

    @staticmethod
    def _map_checkout_status(
        status: str,
    ) -> CheckoutStatus:
        match status:
            case "available":
                return CheckoutStatus.AVAILABLE

            case _:
                raise UnsupportedPaymentStatusError(
                    f"Unsupported Openpay checkout status: {status}"
                )

    @staticmethod
    def _raise_openpay_error(
        response: httpx.Response,
    ) -> None:
        try:
            data = response.json()
        except ValueError as exc:
            raise PaymentProviderError(
                "Openpay returned an invalid error response",
                http_status=response.status_code,
            ) from exc

        error_code = data.get("error_code")
        description = data.get(
            "description",
            "Openpay request failed",
        )

        code = (
            str(error_code)
            if error_code is not None
            else None
        )

        if (
            error_code is not None
            and 3000 <= int(error_code) < 4000
        ):
            raise PaymentDeclinedError(
                description,
                code=code,
                http_status=response.status_code,
            )

        raise PaymentProviderError(
            description,
            code=code,
            http_status=response.status_code,
        )

    @staticmethod
    def _parse_openpay_datetime(
        value: str,
    ) -> datetime:
        return datetime.fromisoformat(
            value
        )