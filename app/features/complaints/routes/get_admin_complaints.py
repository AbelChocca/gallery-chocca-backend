
from typing import Annotated

from fastapi import Depends, Query

from app.features.complaints.complaint_router import router

from app.features.complaints.dependencies.services import (
    get_complaint_service,
    ComplaintService
)
from app.features.complaints.schemas.complaint import (
    AdminComplaintFiltersSchema,
    AdminComplaintListItemResponseSchema
)
from app.shared.pagination.schema import PaginatedResponseSchema

from app.core.authorization.dependencies import (
    require_permission,
)
from app.core.authorization.permissions import Permission
from app.features.complaints.types.complaint import ComplaintFilters


@router.get(
    "/admin",
    summary="Get admin complaints",
    response_model=PaginatedResponseSchema[AdminComplaintListItemResponseSchema],
    dependencies=[
        require_permission(Permission.COMPLAINT_VIEW),
    ],
)
async def get_admin_complaints(
    service: Annotated[
        ComplaintService,
        Depends(get_complaint_service),
    ],
    filters: Annotated[
        AdminComplaintFiltersSchema,
        Depends(),
    ],
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> PaginatedResponseSchema[AdminComplaintListItemResponseSchema]:

    result = await service.get_admin_complaints(
        filters=ComplaintFilters(
            **filters.model_dump()
        ),
        page=page,
        limit=limit,
    )

    return PaginatedResponseSchema[AdminComplaintListItemResponseSchema].model_validate(
        result
    )
