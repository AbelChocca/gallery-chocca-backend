
from typing import Annotated

from fastapi import Depends, Path

from app.features.complaints.complaint_router import router

from app.features.complaints.dependencies.use_cases.send_admin_complaint_response import (
    get_send_admin_complaint_response_use_case,
)

from app.features.complaints.use_cases.send_admin_complaint_response import (
    SendAdminComplaintResponseUseCase,
)

from app.features.complaints.schemas.complaint_response import (
    ComplaintResponseSchema,
)

from app.core.authorization.dependencies import (
    require_permission,
)
from app.core.authorization.permissions import Permission


@router.post(
    "/admin/{complaint_id}/responses/{response_id}/send",
    summary="Send admin complaint response by email",
    response_model=ComplaintResponseSchema,
    dependencies=[
        require_permission(Permission.COMPLAINT_RESPOND),
    ],
)
async def send_admin_complaint_response(
    complaint_id: Annotated[int, Path(gt=0)],
    response_id: Annotated[int, Path(gt=0)],
    case: Annotated[
        SendAdminComplaintResponseUseCase,
        Depends(get_send_admin_complaint_response_use_case),
    ],
) -> ComplaintResponseSchema:

    result = await case.execute(
        complaint_id=complaint_id,
        response_id=response_id,
    )

    return ComplaintResponseSchema.model_validate(
        result
    )
