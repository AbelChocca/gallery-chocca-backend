from app.features.payments.entities.payment_event import PaymentEvent
from app.features.payments.repositories.payment_event_repository import (
    PaymentEventRepository,
)
from datetime import datetime, timezone
from app.features.payments.types.payment_provider import PaymentProvider

class PaymentEventService:

    def __init__(
        self,
        repository: PaymentEventRepository,
    ) -> None:
        self._repository = repository

    async def add(
        self,
        *,
        payment_id: int | None,
        provider: PaymentProvider,
        event_type: str,
        payload: dict,
        provider_event_id: str | None = None,
        flush: bool = True,
    ) -> PaymentEvent:
        event = PaymentEvent(
            id=None,
            payment_id=payment_id,
            provider=provider,
            event_type=event_type,
            provider_event_id=provider_event_id,
            payload=payload,
            created_at=datetime.now(
                timezone.utc
            ),
        )

        return await self._repository.save(
            event,
            flush=flush,
        )

    async def save(
        self,
        event: PaymentEvent,
        flush: bool = True,
    ) -> PaymentEvent:
        return await self._repository.save(
            event,
            flush=flush,
        )

    async def get_by_provider_event_id(
        self,
        provider_event_id: str,
    ) -> PaymentEvent | None:
        return await (
            self._repository
            .get_by_provider_event_id(
                provider_event_id,
            )
        )

    async def get_by_payment_ids(
        self,
        payment_ids: list[int],
    ) -> list[PaymentEvent]:
        return await self._repository.get_by_payment_ids(
            payment_ids
        )