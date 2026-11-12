
from typing import Annotated

from fastapi import Depends, Path

from app.features.complaints.complaint_router import router

from app.features.complaints.dependencies.services import (
    get_complaint_service,
    ComplaintService
)
from app.features.complaints.schemas.complaint import (
    AdminComplaintDetailResponseSchema,
)

from app.core.authorization.dependencies import (
    require_permission,
)
from app.core.authorization.permissions import Permission


@router.get(
    "/admin/{complaint_id}",
    summary="Get admin complaint detail",
    response_model=AdminComplaintDetailResponseSchema,
    dependencies=[
        require_permission(Permission.COMPLAINT_VIEW),
    ],
)
async def get_admin_complaint_detail(
    complaint_id: Annotated[int, Path(gt=0)],
    service: Annotated[
        ComplaintService,
        Depends(get_complaint_service),
    ],
) -> AdminComplaintDetailResponseSchema:

    result = await service.get_by_id(
        complaint_id=complaint_id,
    )

    return AdminComplaintDetailResponseSchema.model_validate(
        result
    )
