from app.api.v1.user.user_route import router
from app.api.schemas.user.user_schema import ReadUserSchema
from app.api.dependencies.user.case_depends import get_user_by_id_case
from app.application.user.cases.get_user_by_id import GetUserByIDCase
from app.api.security.resolvers.sessions import get_admin_session

from fastapi import status, Depends, Path
from typing import Annotated

@router.get(
    "/{user_id}",
    response_model=ReadUserSchema,
    status_code=status.HTTP_200_OK,
    summary="Get an user by her id"
)
async def get_user_by_id(
    user_id: Annotated[int, Path(...)],
    case: Annotated[GetUserByIDCase, Depends(get_user_by_id_case)],
    _: Annotated[None, Depends(get_admin_session)]
) -> ReadUserSchema:
    user_dto = await case.execute(user_id)
    
    return ReadUserSchema(**user_dto)