# app/features/payments/mappers/payment_event_mapper.py

from app.features.payments.entities.payment_event import (
    PaymentEvent,
)
from app.features.payments.models.payment_events import (
    PaymentEventTable,
)

from app.infra.db.mappers.base_mapper import (
    BaseMapper,
)


class PaymentEventMapper(
    BaseMapper[
        PaymentEvent,
        PaymentEventTable,
    ]
):

    @staticmethod
    def to_db_model(
        entity: PaymentEvent,
        existing_model: PaymentEventTable | None = None,
    ) -> PaymentEventTable:
        if existing_model is None:
            return PaymentEventTable(
                id=entity.id,
                payment_id=entity.payment_id,
                provider=entity.provider,
                event_type=entity.event_type,
                provider_event_id=entity.provider_event_id,
                payload=entity.payload,
                created_at=entity.created_at,
            )

        existing_model.payment_id = (
            entity.payment_id
        )

        existing_model.provider = (
            entity.provider
        )

        existing_model.event_type = (
            entity.event_type
        )

        existing_model.provider_event_id = (
            entity.provider_event_id
        )

        existing_model.payload = (
            entity.payload
        )

        existing_model.created_at = (
            entity.created_at
        )

        return existing_model

    @staticmethod
    def to_entity(
        model: PaymentEventTable,
    ) -> PaymentEvent:
        return PaymentEvent(
            id=model.id,

            payment_id=model.payment_id,

            provider=model.provider,

            event_type=model.event_type,

            provider_event_id=(
                model.provider_event_id
            ),

            payload=model.payload,

            created_at=model.created_at,
        )