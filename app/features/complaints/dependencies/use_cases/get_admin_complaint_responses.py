from typing import Annotated

from fastapi import Depends


from app.features.complaints.use_cases.get_admin_complaint_responses import (
    GetAdminComplaintResponsesUseCase,
)

from app.features.complaints.dependencies.services import (
    get_complaint_service,
    get_complaint_response_service,
    ComplaintService,
    ComplaintResponseService
)


def get_admin_complaint_responses_use_case(
    complaint_service: Annotated[
        ComplaintService,
        Depends(get_complaint_service),
    ],
    complaint_response_service: Annotated[
        ComplaintResponseService,
        Depends(get_complaint_response_service),
    ],
) -> GetAdminComplaintResponsesUseCase:

    return GetAdminComplaintResponsesUseCase(
        complaint_service=complaint_service,
        complaint_response_service=complaint_response_service,
    )
