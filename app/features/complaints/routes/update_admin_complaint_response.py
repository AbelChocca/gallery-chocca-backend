
from typing import Annotated

from fastapi import Depends, Path

from app.features.complaints.complaint_router import router
from app.features.complaints.dependencies.use_cases.update_admin_complaint_response import (
    get_update_admin_complaint_response_use_case,
)
from app.features.complaints.use_cases.update_admin_complaint_response import (
    UpdateAdminComplaintResponseUseCase,
)
from app.features.complaints.schemas.complaint_response import (
    UpdateComplaintResponseRequestSchema,
    ComplaintResponseSchema,
)

from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission


@router.patch(
    "/admin/{complaint_id}/responses/{response_id}",
    summary="Update admin complaint response draft",
    response_model=ComplaintResponseSchema,
    dependencies=[
        require_permission(Permission.COMPLAINT_RESPOND),
    ],
)
async def update_admin_complaint_response(
    complaint_id: Annotated[int, Path(gt=0)],
    response_id: Annotated[int, Path(gt=0)],
    payload: UpdateComplaintResponseRequestSchema,
    case: Annotated[
        UpdateAdminComplaintResponseUseCase,
        Depends(get_update_admin_complaint_response_use_case),
    ],
) -> ComplaintResponseSchema:

    result = await case.execute(
        complaint_id=complaint_id,
        response_id=response_id,
        message=payload.message,
    )

    return ComplaintResponseSchema.model_validate(result)
