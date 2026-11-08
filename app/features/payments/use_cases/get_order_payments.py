from app.features.payments.services.payment_service import (
    PaymentService,
)
from app.features.payments.services.payment_event_service import (
    PaymentEventService,
)

from app.features.payments.types.payment import (
    PaymentDetailDTO,
    PaymentEventDetailDTO,
)


class GetOrderPaymentsUseCase:

    def __init__(
        self,
        *,
        payment_service: PaymentService,
        payment_event_service: PaymentEventService,
    ) -> None:
        self._payment_service = payment_service
        self._payment_event_service = (
            payment_event_service
        )

    async def execute(
        self,
        *,
        order_id: int,
    ) -> list[PaymentDetailDTO]:

        payments = (
            await self._payment_service.get_by_order_id(
                order_id
            )
        )

        if not payments:
            return []

        payment_ids = [
            payment.id
            for payment in payments
            if payment.id is not None
        ]

        events = (
            await self._payment_event_service
            .get_by_payment_ids(
                payment_ids
            )
        )

        events_by_payment_id: dict[
            int,
            list[PaymentEventDetailDTO],
        ] = {}

        for event in events:
            if event.payment_id is None:
                continue

            events_by_payment_id.setdefault(
                event.payment_id,
                [],
            ).append(
                PaymentEventDetailDTO(
                    id=event.id,
                    provider=event.provider,
                    event_type=event.event_type,
                    provider_event_id=(
                        event.provider_event_id
                    ),
                    payload=event.payload,
                    created_at=event.created_at,
                )
            )

        return [
            PaymentDetailDTO(
                id=payment.id,
                order_id=payment.order_id,

                provider=payment.provider,
                payment_method=(
                    payment.payment_method
                ),
                status=payment.status,

                amount=payment.amount,
                currency=payment.currency,

                provider_order_id=(
                    payment.provider_order_id
                ),
                provider_payment_id=(
                    payment.provider_payment_id
                ),

                checkout_id=payment.checkout_id,
                payment_link=payment.payment_link,
                expires_at=payment.expires_at,

                authorization=payment.authorization,

                error_code=payment.error_code,
                error_message=(
                    payment.error_message
                ),

                created_at=payment.created_at,
                updated_at=payment.updated_at,

                events=events_by_payment_id.get(
                    payment.id,
                    [],
                ),
            )
            for payment in payments
            if payment.id is not None
        ]