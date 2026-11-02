from app.features.orders.entities.order_receipt import (
    OrderReceipt,
)
from app.features.orders.repositories.order_receipt_repository import (
    OrderReceiptRepository,
)
from datetime import datetime, timezone
from app.features.orders.types.order_receipt import ReceiptStatus


class OrderReceiptService:

    def __init__(
        self,
        repository: OrderReceiptRepository,
    ) -> None:
        self._repository = repository

    async def mark_as_issuing(
        self,
        *,
        receipt: OrderReceipt,
        flush: bool = True,
    ) -> OrderReceipt:

        receipt.status = ReceiptStatus.ISSUING

        receipt.provider_error_code = None
        receipt.provider_error_message = None

        receipt.updated_at = datetime.now(timezone.utc)

        return await self._repository.save(
            receipt,
            flush=flush,
        )


    async def mark_as_issued(
        self,
        *,
        receipt: OrderReceipt,
        external_id: str,
        series_number: str,
        flush: bool = True,
    ) -> OrderReceipt:

        now = datetime.now(timezone.utc)

        receipt.status = ReceiptStatus.ISSUED

        receipt.external_id = external_id
        receipt.series_number = series_number

        receipt.provider_error_code = None
        receipt.provider_error_message = None

        receipt.issued_at = now
        receipt.updated_at = now

        return await self._repository.save(
            receipt,
            flush=flush,
        )


    async def mark_as_retry_pending(
        self,
        *,
        receipt: OrderReceipt,
        external_id: str | None = None,
        series_number: str | None = None,
        provider_error_code: str | None = None,
        provider_error_message: str | None = None,
        flush: bool = True,
    ) -> OrderReceipt:

        receipt.status = ReceiptStatus.RETRY_PENDING

        if external_id is not None:
            receipt.external_id = external_id

        if series_number is not None:
            receipt.series_number = series_number

        receipt.provider_error_code = (
            provider_error_code
        )
        receipt.provider_error_message = (
            provider_error_message
        )

        receipt.updated_at = datetime.now(timezone.utc)

        return await self._repository.save(
            receipt,
            flush=flush,
        )

    async def mark_email_sent(
        self,
        *,
        receipt: OrderReceipt,
        provider_id: str,
        flush: bool = True,
    ) -> OrderReceipt:

        receipt.email_provider_id = provider_id
        receipt.email_sent_at = (
            datetime.now(timezone.utc)
        )
        receipt.email_error_message = None

        return await self._repository.save(
            receipt,
            flush=flush,
        )

    async def mark_email_failed(
        self,
        *,
        receipt: OrderReceipt,
        error_message: str,
        flush: bool = True,
    ) -> OrderReceipt:

        receipt.email_sent_at = None
        receipt.email_error_message = (
            error_message
        )

        return await self._repository.save(
            receipt,
            flush=flush,
        )

    async def mark_as_failed(
        self,
        *,
        receipt: OrderReceipt,
        provider_error_code: str | None = None,
        provider_error_message: str | None = None,
        flush: bool = True,
    ) -> OrderReceipt:

        receipt.status = ReceiptStatus.FAILED

        receipt.provider_error_code = (
            provider_error_code
        )
        receipt.provider_error_message = (
            provider_error_message
        )

        receipt.updated_at = datetime.now(timezone.utc)

        return await self._repository.save(
            receipt,
            flush=flush,
        )


    async def create(
        self,
        *,
        order_id: int,
        flush: bool = True,
    ) -> OrderReceipt:

        now = datetime.now(timezone.utc)

        receipt = OrderReceipt(
            order_id=order_id,
            status=ReceiptStatus.PENDING,
            created_at=now,
            updated_at=now,
        )

        return await self._repository.save(
            receipt,
            flush=flush,
        )

    async def get_by_order_id(
        self,
        *,
        order_id: int,
        raises: bool = True,
        with_lock: bool = False,
    ) -> OrderReceipt | None:
        return await (
            self._repository.get_by_order_id(
                order_id=order_id,
                raises=raises,
                with_lock=with_lock,
            )
        )