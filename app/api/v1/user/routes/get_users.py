from app.api.v1.user.user_route import router
from app.api.schemas.user.user_schema import GetUsersResponseSchema
from app.api.schemas.pagination import PaginationSchema
from app.application.user.cases.get_users import GetUsersCase
from app.api.dependencies.user.case_depends import get_users_case
from app.api.security.resolvers.sessions import get_admin_session

from fastapi import status, Depends, Query
from typing import Annotated

@router.get(
    "/",
    response_model=GetUsersResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Get users endpoint"
)
async def get_users(
    case: Annotated[GetUsersCase, Depends(get_users_case)],
    pagination: Annotated[PaginationSchema, Depends()],
    _: Annotated[None, Depends(get_admin_session)],
    related_name: Annotated[str, Query(..., min_length=2, max_length=50)] = None
) -> GetUsersResponseSchema:
    response_dto = await case.execute(
        related_name=related_name,
        page=pagination.page,
        limit=pagination.limit
    )
    return GetUsersResponseSchema(**response_dto)