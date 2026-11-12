
from typing import Annotated

from fastapi import Depends, Path

from app.features.complaints.complaint_router import router

from app.features.complaints.dependencies.use_cases.get_admin_complaint_responses import (
    get_admin_complaint_responses_use_case,
)
from app.features.complaints.use_cases.get_admin_complaint_responses import (
    GetAdminComplaintResponsesUseCase,
)

from app.features.complaints.schemas.complaint_response import (
    ComplaintResponseSchema,
)

from app.core.authorization.dependencies import (
    require_permission,
)
from app.core.authorization.permissions import Permission


@router.get(
    "/admin/{complaint_id}/responses",
    summary="Get admin complaint responses",
    response_model=list[ComplaintResponseSchema],
    dependencies=[
        require_permission(Permission.COMPLAINT_VIEW),
    ],
)
async def get_admin_complaint_responses(
    complaint_id: Annotated[int, Path(gt=0)],
    case: Annotated[
        GetAdminComplaintResponsesUseCase,
        Depends(get_admin_complaint_responses_use_case),
    ],
) -> list[ComplaintResponseSchema]:

    result = await case.execute(
        complaint_id=complaint_id,
    )

    return [
        ComplaintResponseSchema.model_validate(response)
        for response in result
    ]
