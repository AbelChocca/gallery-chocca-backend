from app.api.v1.user.user_route import router
from app.api.schemas.user.user_schema import ReadUserSchema
from app.api.security.resolvers.sessions import get_admin_session

from fastapi import status, Depends
from typing import Annotated

@router.get(
    '/admin',
    status_code=status.HTTP_200_OK,
    response_model=ReadUserSchema,
    summary="Endpoint for check admin session"
)
async def get_info(
    admin_dto: Annotated[dict, Depends(get_admin_session)]
) -> ReadUserSchema:
    return ReadUserSchema(**admin_dto)