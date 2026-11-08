
from datetime import datetime, timezone

from app.features.complaints.entities.complaint_response import (
    ComplaintResponse,
)
from app.features.complaints.repositories.complaint_response_repository import (
    ComplaintResponseRepository,
)
from app.features.complaints.types.complaint_response import (
    ComplaintResponseStatus,
)

from app.core.exceptions import InvalidOperation


class ComplaintResponseService:
    def __init__(
        self,
        repository: ComplaintResponseRepository,
    ):
        self._repository = repository

    async def reserve_send(
        self,
        *,
        response_id: int,
        complaint_id: int,
    ) -> ComplaintResponse:

        response = await self.get_by_id(
            response_id=response_id,
            raises=True,
            with_lock=True,
        )

        if response.complaint_id != complaint_id:
            raise InvalidOperation(
                message="La respuesta no pertenece a esta reclamación."
            )

        if response.status != ComplaintResponseStatus.DRAFT:
            raise InvalidOperation(
                message="Solo se pueden enviar respuestas en borrador."
            )

        response.status = ComplaintResponseStatus.PENDING_SEND

        return await self._repository.save(
            response,
            flush=True,
        )


    async def create_draft(
        self,
        *,
        complaint_id: int,
        message: str,
        author_user_id: int | None,
        recipient_email: str | None,
    ) -> ComplaintResponse:
        response = ComplaintResponse(
            complaint_id=complaint_id,
            message=message,
            author_user_id=author_user_id,
            recipient_email=recipient_email,
            status=ComplaintResponseStatus.DRAFT,
            created_at=datetime.now(timezone.utc),
        )

        return await self._repository.save(
            response,
            flush=True,
        )

    async def get_by_id(
        self,
        response_id: int,
        *,
        raises: bool = True,
        with_lock: bool = False,
    ) -> ComplaintResponse | None:
        return await self._repository.get_by_id(
            model_id=response_id,
            raises=raises,
            with_lock=with_lock,
        )

    async def get_by_complaint_id(
        self,
        complaint_id: int,
    ) -> list[ComplaintResponse]:
        return await self._repository.get_by_complaint_id(
            complaint_id
        )

    async def mark_sent(
        self,
        *,
        response_id: int,
        external_message_id: str,
        now: datetime | None = None,
    ) -> ComplaintResponse:
        response = await self._repository.get_by_id(
            response_id,
            with_lock=True,
        )

        if response.status != ComplaintResponseStatus.PENDING_SEND:
            raise InvalidOperation(
                message="La respuesta no está pendiente de envío."
            )

        response.status = ComplaintResponseStatus.SENT
        response.external_message_id = external_message_id
        response.error_message = None
        response.sent_at = now or datetime.now(timezone.utc)

        return await self._repository.save(
            response,
            flush=True,
        )

    async def update_draft(
        self,
        *,
        response_id: int,
        complaint_id: int,
        message: str,
    ) -> ComplaintResponse:

        response = await self._repository.get_by_id(
            model_id=response_id,
            raises=True,
            with_lock=True,
        )

        if response.complaint_id != complaint_id:
            raise InvalidOperation(
                message="La respuesta no pertenece a esta reclamación."
            )

        if response.status != ComplaintResponseStatus.DRAFT:
            raise InvalidOperation(
                message="Solo pueden modificarse respuestas en borrador."
            )

        response.message = message.strip()

        return await self._repository.save(
            response,
            flush=True,
        )


    async def mark_failed(
        self,
        *,
        response_id: int,
        error_message: str,
    ) -> ComplaintResponse:
        response = await self._repository.get_by_id(
            response_id,
            with_lock=True,
        )

        if response.status != ComplaintResponseStatus.PENDING_SEND:
            raise InvalidOperation(
                message="La respuesta no está pendiente de envío."
            )

        response.status = ComplaintResponseStatus.DELIVERY_FAILED
        response.error_message = error_message

        return await self._repository.save(
            response,
            flush=True,
        )
