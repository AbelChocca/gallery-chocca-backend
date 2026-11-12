from datetime import datetime, timezone
from decimal import Decimal

from app.features.payments.entities.payment import Payment
from app.features.payments.providers.base_provider import (
    BasePaymentProvider,
)
from app.features.payments.repositories.payment_repository import (
    PaymentRepository,
)
from app.features.payments.types.payment_provider import (
    CheckoutResult,
    CreateCheckoutRequest,
    CreateCardChargeRequest,
    CardChargeCustomer,
    CardChargeResult
)
from app.features.payments.types.payment import PaymentMethod, PaymentStatus
from app.features.payments.types.payment_provider import PaymentProvider
from app.core.settings.pydantic_settings import settings



class PaymentService:
    def __init__(
        self,
        payment_repository: PaymentRepository,
        payment_provider: BasePaymentProvider,
    ) -> None:
        self._payment_repository = payment_repository
        self._payment_provider = payment_provider

    async def mark_succeeded(
        self,
        *,
        payment: Payment,
        provider_payment_id: str,
        authorization: str | None,
        flush: bool = True,
    ) -> Payment:
        payment.status = PaymentStatus.PAID
        payment.provider_payment_id = (
            provider_payment_id
        )
        payment.authorization = authorization

        payment.error_code = None
        payment.error_message = None

        payment.updated_at = datetime.now(
            timezone.utc
        )

        return await self._payment_repository.save(
            payment,
            flush=flush,
        )

    async def mark_failed(
        self,
        *,
        payment: Payment,
        provider_payment_id: str,
        error_message: str | None,
        error_code: str | None = None,
        flush: bool = True,
    ) -> Payment:
        payment.status = PaymentStatus.FAILED

        payment.provider_payment_id = (
            provider_payment_id
        )

        payment.error_code = error_code
        payment.error_message = (
            error_message
        )

        payment.updated_at = datetime.now(
            timezone.utc
        )

        return await self._payment_repository.save(
            payment,
            flush=flush,
        )

    async def add(
        self,
        *,
        order_id: int,
        provider: PaymentProvider,
        payment_method: PaymentMethod,
        status: PaymentStatus,
        amount: Decimal,
        currency: str,
        provider_order_id: str,
        provider_payment_id: str | None = None,
        checkout_id: str | None = None,
        payment_link: str | None = None,
        expires_at: datetime | None = None,
        authorization: str | None = None,
        error_code: str | None = None,
        error_message: str | None = None,
        flush: bool = True,
    ) -> Payment:
        now = datetime.now(timezone.utc)

        payment = Payment(
            id=None,
            order_id=order_id,
            provider=provider,
            payment_method=payment_method,
            status=status,
            amount=amount,
            currency=currency,
            provider_payment_id=provider_payment_id,
            provider_order_id=provider_order_id,
            checkout_id=checkout_id,
            payment_link=payment_link,
            expires_at=expires_at,
            authorization=authorization,
            error_code=error_code,
            error_message=error_message,
            created_at=now,
            updated_at=now,
        )

        return await self._payment_repository.save(
            payment,
            flush=flush,
        )

    async def create_card_charge(
        self,
        *,
        token_id: str,
        device_session_id: str,
        amount: Decimal,
        currency: str,
        description: str,
        provider_order_id: str,
        client_ip: str,
        customer_name: str,
        customer_last_name: str,
        customer_phone: str,
        customer_email: str,
        order_id: int,
        use_3d_secure: bool = True,
    ) -> CardChargeResult:
        request = CreateCardChargeRequest(
            token_id=token_id,
            device_session_id=device_session_id,
            amount=amount,
            currency=currency,
            description=description,
            order_id=provider_order_id,
            client_ip=client_ip,
            customer=CardChargeCustomer(
                name=customer_name,
                last_name=customer_last_name,
                phone_number=customer_phone,
                email=customer_email,
            ),
            use_3d_secure=use_3d_secure,
            redirect_url=(
                f"{settings.FRONTEND_URL}"
                f"/checkout/order/{order_id}/payment/result"
            )
            if use_3d_secure
            else None,
        )

        return await self._payment_provider.create_card_charge(
            request
        )

    async def update_charge_result(
        self,
        *,
        payment: Payment,
        provider_payment_id: str | None,
        authorization: str | None,
        error_message: str | None,
        flush: bool = True,
    ) -> Payment:
        payment.provider_payment_id = provider_payment_id
        payment.authorization = authorization
        payment.error_message = error_message
        payment.updated_at = datetime.now(timezone.utc)

        return await self._payment_repository.save(
            payment,
            flush=flush,
        )

    async def get_by_provider_order_id(
        self,
        provider_order_id: str,
        raises: bool = True,
    ) -> Payment | None:
        return await (
            self._payment_repository
            .get_by_provider_order_id(
                provider_order_id,
                raises=raises,
            )
        )

    async def create_checkout(
        self,
        request: CreateCheckoutRequest,
    ) -> CheckoutResult:
        return await self._payment_provider.create_checkout(
            request
        )

    async def get_by_id(
        self,
        payment_id: int,
        raises: bool = True,
        with_lock: bool = False,
    ) -> Payment | None:
        return await self._payment_repository.get_by_id(
            payment_id,
            raises=raises,
            with_lock=with_lock,
        )

    async def get_by_provider_payment_id(
        self,
        provider_payment_id: str,
        raises: bool = True,
    ) -> Payment | None:
        return await (
            self._payment_repository
            .get_by_provider_payment_id(
                provider_payment_id,
                raises=raises,
            )
        )

    async def get_by_order_id(
        self,
        order_id: int,
    ) -> list[Payment]:
        return await self._payment_repository.get_by_order_id(
            order_id,
        )

    async def delete_by_id(
        self,
        payment_id: int,
    ) -> None:
        await self._payment_repository.delete_by_id(
            payment_id,
        )