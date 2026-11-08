
from typing import Annotated

from fastapi import Depends

from app.features.complaints.services.complaint_service import (
    ComplaintService,
)
from app.features.complaints.services.complaint_response_service import (
    ComplaintResponseService,
)

from app.features.complaints.dependencies.services import (
    get_complaint_service,
    get_complaint_response_service,
)

from app.features.complaints.use_cases.create_admin_complaint_response import (
    CreateAdminComplaintResponseUseCase,
)


def get_create_admin_complaint_response_use_case(
    complaint_service: Annotated[
        ComplaintService,
        Depends(get_complaint_service),
    ],
    complaint_response_service: Annotated[
        ComplaintResponseService,
        Depends(get_complaint_response_service),
    ],
) -> CreateAdminComplaintResponseUseCase:

    return CreateAdminComplaintResponseUseCase(
        complaint_service=complaint_service,
        complaint_response_service=complaint_response_service,
    )
