from uuid import uuid4

from app.core.exceptions import (
    InvalidOperation,
    ValueNotFound,
)

from app.features.orders.services.order_service import (
    OrderService,
)
from app.features.orders.types.order import (
    OrderStatus,
)

from app.features.customer.customer_service import (
    CustomerService,
)

from app.features.payments.services.payment_service import (
    PaymentService,
)

from app.features.payments.types.payment import (
    PaymentProvider,
    PaymentStatus,
    PaymentMethod,
    CreateCardChargeResult,
)

class CreateCardChargeUseCase:
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
        token_id: str,
        device_session_id: str,
        client_ip: str,
        user_id: int | None,
        session_id: str | None,
    ) -> CreateCardChargeResult:

        customer = None

        if user_id is not None:
            customer = await self._customer_service.get_by_user_id(
                user_id
            )

        elif session_id is not None:
            customer = await self._customer_service.get_by_session_id(
                session_id
            )

        if customer is None:
            raise ValueNotFound(
                message="Cliente no encontrado.",
            )

        order = await self._order_service.get_by_id(
            order_id=order_id,
            raises=False,
        )

        if order is None:
            raise ValueNotFound(
                message="Pedido no encontrado.",
            )

        if order.customer_id != customer.id:
            raise ValueNotFound(
                message="Pedido no encontrado.",
            )

        if order.status != OrderStatus.PENDING_PAYMENT:
            raise InvalidOperation(
                message=(
                    "El pedido no está pendiente "
                    "de pago."
                ),
            )

        if order.payment_method != PaymentMethod.CARD:
            raise InvalidOperation(
                message=(
                    "El pedido no fue creado "
                    "para pago con tarjeta."
                ),
            )

        provider_order_id = (
            f"{order.order_number}-"
            f"{uuid4().hex[:8]}"
        )

        payment = await self._payment_service.add(
            order_id=order.id,
            provider=PaymentProvider.OPENPAY,
            payment_method=PaymentMethod.CARD,
            status=PaymentStatus.PENDING,
            amount=order.total,
            currency="PEN",
            provider_order_id=provider_order_id,
        )

        charge = await self._payment_service.create_card_charge(
            token_id=token_id,
            device_session_id=device_session_id,

            amount=order.total,
            currency="PEN",

            description=(
                f"Pedido {order.order_number}"
            ),

            provider_order_id=provider_order_id,

            client_ip=client_ip,

            customer_name=customer.name,
            customer_last_name=customer.last_name,
            customer_phone=customer.phone,
            customer_email=customer.email,

            order_id=order.id,

            use_3d_secure=False,
        )

        await self._payment_service.update_charge_result(
            payment=payment,
            provider_payment_id=charge.provider_payment_id,
            authorization=charge.authorization,
            error_message=charge.error_message,
        )

        return CreateCardChargeResult(
            payment_id=payment.id,
            order_id=order.id,
            status=charge.status,
            redirect_url=charge.redirect_url,
        )