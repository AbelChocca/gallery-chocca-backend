from app.features.complaints.entities.complaint_response import (
    ComplaintResponse,
)

from app.features.complaints.services.complaint_service import (
    ComplaintService,
)
from app.features.complaints.services.complaint_response_service import (
    ComplaintResponseService,
)


class GetAdminComplaintResponsesUseCase:

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
    ) -> list[ComplaintResponse]:

        await self._complaint_service.get_by_id(
            complaint_id=complaint_id,
            raises=True,
        )

        return await (
            self._complaint_response_service.get_by_complaint_id(
                complaint_id
            )
        )
