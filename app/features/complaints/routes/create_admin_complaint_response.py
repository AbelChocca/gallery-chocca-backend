
from typing import Annotated

from fastapi import Depends, Path, status

from app.features.complaints.complaint_router import router

from app.features.complaints.dependencies.use_cases.create_admin_complaint_response import (
    get_create_admin_complaint_response_use_case,
)

from app.features.complaints.use_cases.create_admin_complaint_response import (
    CreateAdminComplaintResponseUseCase,
)

from app.features.complaints.schemas.complaint_response import (
    CreateComplaintResponseRequestSchema,
    ComplaintResponseSchema,
)

from app.core.authorization.dependencies import (
    require_permission,
)
from app.core.authorization.permissions import Permission

from app.api.security.resolvers.sessions import get_user_id


@router.post(
    "/admin/{complaint_id}/responses",
    status_code=status.HTTP_201_CREATED,
    summary="Create admin complaint response draft",
    response_model=ComplaintResponseSchema,
    dependencies=[
        require_permission(Permission.COMPLAINT_RESPOND),
    ],
)
async def create_admin_complaint_response(
    complaint_id: Annotated[int, Path(gt=0)],
    payload: CreateComplaintResponseRequestSchema,
    case: Annotated[
        CreateAdminComplaintResponseUseCase,
        Depends(
            get_create_admin_complaint_response_use_case
        ),
    ],
    author_user_id: Annotated[
        int,
        Depends(get_user_id),
    ],
) -> ComplaintResponseSchema:

    result = await case.execute(
        complaint_id=complaint_id,
        message=payload.message,
        author_user_id=author_user_id,
    )

    return ComplaintResponseSchema.model_validate(
        result
    )
