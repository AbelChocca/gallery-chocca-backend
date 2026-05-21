from app.features.user.user_route import router
from app.api.security.auth.schema import ReadSessionSchema
from app.api.security.resolvers.sessions import get_user_session

from fastapi import status, Depends
from typing import Annotated

@router.get(
    '/me',
    status_code=status.HTTP_200_OK,
    response_model=ReadSessionSchema,
    summary="Endpoint for user's info"
)
async def get_info(
    user_dto: Annotated[dict, Depends(get_user_session)]
) -> ReadSessionSchema:
    return ReadSessionSchema(**user_dto)