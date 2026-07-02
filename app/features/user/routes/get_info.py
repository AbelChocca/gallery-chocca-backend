from app.features.user.user_route import router
from app.features.user.user_schema import ReadUserSchema
from app.api.security.resolvers.sessions import get_user_info

from fastapi import status, Depends
from typing import Annotated

@router.get(
    '/me',
    status_code=status.HTTP_200_OK,
    response_model=ReadUserSchema,
    summary="Endpoint for user's info"
)
async def get_info(
    user_info: Annotated[ReadUserSchema, Depends(get_user_info)]
) -> ReadUserSchema:
    return user_info