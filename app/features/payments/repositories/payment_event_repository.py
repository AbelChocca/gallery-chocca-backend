# app/features/payments/repositories/postgres_payment_event_repository.py

from sqlalchemy import select

from app.features.payments.entities.payment_event import (
    PaymentEvent,
)
from app.features.payments.models.payment_events import (
    PaymentEventTable,
)

from app.infra.db.repositories.base_repository import (
    BaseRepository,
)


class PaymentEventRepository(
    BaseRepository[
        PaymentEvent,
        PaymentEventTable,
    ],
):

    async def get_by_provider_event_id(
        self,
        provider_event_id: str,
    ) -> PaymentEvent | None:
        stmt = (
            select(PaymentEventTable)
            .where(
                PaymentEventTable.provider_event_id
                == provider_event_id
            )
        )

        result = await self._db_session.execute(
            stmt
        )

        model = (
            result.scalar_one_or_none()
        )

        if model is None:
            return None

        return self._base_mapper.to_entity(
            model
        )

    async def get_by_payment_ids(
        self,
        payment_ids: list[int],
    ) -> list[PaymentEvent]:

        if not payment_ids:
            return []

        stmt = (
            select(PaymentEventTable)
            .where(
                PaymentEventTable.payment_id.in_(
                    payment_ids
                )
            )
            .order_by(
                PaymentEventTable.created_at.asc()
            )
        )

        result = await self._db_session.execute(
            stmt
        )

        models = result.scalars().all()

        return [
            self._base_mapper.to_entity(model)
            for model in models
        ]