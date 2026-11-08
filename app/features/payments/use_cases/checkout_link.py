from datetime import datetime, timezone
from uuid import uuid4

from app.features.customer.customer_service import (
    CustomerService,
)

from app.features.orders.services.order_service import (
    OrderService,
)
from app.features.orders.types.order import (
    OrderStatus,
)

from app.features.payments.types.payment import (
    CreatePaymentCheckoutInput,
    CreatePaymentCheckoutResult,
    PaymentProvider,
    PaymentStatus,
)

from app.features.payments.entities.payment import (
    Payment,
)

from app.features.payments.services.payment_service import (
    PaymentService,
)

from app.features.payments.types.payment_provider import (
    CheckoutCustomer,
    CreateCheckoutRequest,
)

from app.core.exceptions import (
    ValidationError,
    ValueNotFound,
)

from app.core.settings.pydantic_settings import settings

class CreatePaymentCheckoutUseCase:

    def __init__(
        self,
        *,
        order_service: OrderService,
        customer_service: CustomerService,
        payment_service: PaymentService,
    ) -> None:
        self._order_service = order_service
        self._customer_service = customer_service
        self._payment_service = payment_service

    async def execute(
        self,
        *,
        order_id: int,
        input: CreatePaymentCheckoutInput,
    ) -> CreatePaymentCheckoutResult:

        order = await self._order_service.get_by_id(
            order_id,
        )

        if order is None:
            raise ValueNotFound(
                "Pedido no encontrado.",
                context={
                    "order_id": order_id,
                },
            )

        if order.id is None:
            raise ValueNotFound(
                "El ID del pedido no se envio.",
                context={
                    "order_id": order_id,
                },
            )

        if (
            order.status
            != OrderStatus.PENDING_PAYMENT
        ):
            raise ValidationError(
                "El pedido no esta pendiendo de pago."
            )

        if order.customer_id is None:
            raise ValueNotFound(
                "No se encontro cliente asociado al pedido.",
                context={
                    "order_id": order.id,
                },
            )

        existing_payments = (
            await self._payment_service.get_by_order_id(
                order.id
            )
        )

        now = datetime.now(timezone.utc)

        if (
            input.expiration_date is not None
            and input.expiration_date <= now
        ):
            raise ValidationError(
                "La fecha de expiración del link de pago debe ser futura."
            )

        existing = next(
            (
                payment
                for payment in existing_payments
                if (
                    payment.id is not None
                    and payment.status == PaymentStatus.PENDING
                    and payment.checkout_id
                    and payment.payment_link
                    and (
                        payment.expires_at is None
                        or payment.expires_at > now
                    )
                )
            ),
            None,
        )

        if existing is not None:
            return CreatePaymentCheckoutResult(
                payment_id=existing.id,
                status=existing.status,

                amount=existing.amount,
                currency=existing.currency,

                checkout_id=existing.checkout_id,
                checkout_link=existing.payment_link,

                expires_at=existing.expires_at,
            )

        customer = (
            await self._customer_service.get_by_id(
                order.customer_id,
            )
        )

        if customer is None:
            raise ValueNotFound(
                "No se encontro cliente asociado al pedido.",
                context={
                    "order_id": order.id,
                    "customer_id": order.customer_id,
                },
            )

        if not customer.email:
            raise ValidationError(
                "El email del cliente es requerido para el checkout de Openpay."
            )

        if not customer.phone:
            raise ValidationError(
                "El numero de telefono del cliente es requerido para el checkout de Openpay."
            )

        provider_order_id = (
            f"{order.order_number}-{uuid4().hex[:8]}"
        )

        payment = Payment(
            id=None,

            order_id=order.id,

            provider=PaymentProvider.OPENPAY,
            status=PaymentStatus.PENDING,

            amount=order.total,
            currency="PEN",

            provider_payment_id=None,

            provider_order_id=provider_order_id,

            checkout_id=None,
            payment_link=None,
            expires_at=None,

            authorization=None,

            error_code=None,
            error_message=None,

            created_at=now,
            updated_at=now,
        )

        payment = (
            await self._payment_service.save(
                payment,
                flush=True,
            )
        )

        if payment.id is None:
            raise RuntimeError(
                "El ID del pago no fue generado."
            )

        checkout = (
            await self._payment_service.create_checkout(
                CreateCheckoutRequest(
                    amount=payment.amount,
                    currency=payment.currency,

                    description=(
                        f"Pedido {order.order_number}"
                    ),

                    order_id=provider_order_id,

                    redirect_url=(
                        self._build_redirect_url()
                    ),

                    customer=CheckoutCustomer(
                        name=customer.name,
                        last_name=customer.last_name,
                        email=customer.email,
                        phone_number=customer.phone,
                    ),

                    send_email=(
                        input.send_email
                    ),

                    expiration_date=(
                        input.expiration_date
                    ),
                )
            )
        )

        payment.checkout_id = (
            checkout.provider_checkout_id
        )

        payment.payment_link = (
            checkout.checkout_link
        )

        payment.expires_at = (
            checkout.expiration_date
        )

        payment.updated_at = datetime.now(
            timezone.utc
        )

        payment = await self._payment_service.save(
            payment,
            flush=True,
        )

        return CreatePaymentCheckoutResult(
            payment_id=payment.id,

            status=payment.status,

            amount=payment.amount,
            currency=payment.currency,

            checkout_id=(
                checkout.provider_checkout_id
            ),

            checkout_link=(
                checkout.checkout_link
            ),

            expires_at=(
                checkout.expiration_date
            ),
        )

    @staticmethod
    def _build_redirect_url(
    ) -> str:
        base_url = (
            settings.FRONTEND_URL.rstrip("/")
        )

        return (
            f"{base_url}/mis-pedidos"
        )