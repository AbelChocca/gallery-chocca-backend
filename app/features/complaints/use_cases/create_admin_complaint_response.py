from app.core.exceptions import InvalidOperation

from app.features.complaints.entities.complaint_response import (
    ComplaintResponse,
)

from app.features.complaints.services.complaint_service import (
    ComplaintService,
)
from app.features.complaints.services.complaint_response_service import (
    ComplaintResponseService,
)

from app.features.complaints.types.complaint import (
    ComplaintStatus,
)


class CreateAdminComplaintResponseUseCase:

    def __init__(
        self,
        *,
        complaint_service: ComplaintService,
        complaint_response_service: ComplaintResponseService,
    ):
        self._complaint_service = complaint_service
        self._complaint_response_service = complaint_response_service

    async def execute(
        self,
        *,
        complaint_id: int,
        message: str,
        author_user_id: int,
    ) -> ComplaintResponse:

        complaint = await self._complaint_service.get_by_id(
            complaint_id=complaint_id,
            raises=True,
            with_lock=True,
        )

        if complaint.status == ComplaintStatus.RESPONDED:
            raise InvalidOperation(
                message=(
                    "La reclamación ya fue respondida. "
                    "No se pueden crear nuevos borradores."
                ),
            )

        return await self._complaint_response_service.create_draft(
            complaint_id=complaint.id,
            message=message.strip(),
            author_user_id=author_user_id,
            recipient_email=(
                complaint.email
                if complaint.email
                else None
            ),
        )
