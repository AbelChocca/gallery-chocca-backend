from app.features.user.user_route import router
from app.features.user.user_schema import GetUsersResponseSchema
from app.shared.pagination.schema import PaginationSchema
from app.api.security.resolvers.sessions import get_admin_session
from app.features.user.dependency import get_user_service
from app.features.user.service import UserService

from fastapi import status, Depends, Query
from typing import Annotated

@router.get(
    "/",
    response_model=GetUsersResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Get users endpoint"
)
async def get_users(
    service: Annotated[UserService, Depends(get_user_service)],
    pagination: Annotated[PaginationSchema, Depends()],
    _: Annotated[None, Depends(get_admin_session)],
    related_name: Annotated[str, Query(..., min_length=2, max_length=50)] = None
) -> GetUsersResponseSchema:
    response_dict = await service.get_users(
        related_name=related_name,
        page=pagination.page,
        limit=pagination.limit
    )
    return GetUsersResponseSchema(**response_dict)