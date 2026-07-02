from app.features.user.user_route import router
from app.features.user.user_schema import ReadUserSchema
from app.features.user.dependency import get_user_service
from app.features.user.service import UserService
from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission

from fastapi import status, Depends, Path
from typing import Annotated

@router.get(
    "/{user_id}",
    response_model=ReadUserSchema,
    status_code=status.HTTP_200_OK,
    summary="Get an user by her id",
    dependencies=[
        require_permission(Permission.USER_READ)
    ]
)
async def get_user_by_id(
    user_id: Annotated[int, Path(...)],
    service: Annotated[UserService, Depends(get_user_service)]
) -> ReadUserSchema:
    user_dict = await service.get_user_by_id(user_id)
    
    return ReadUserSchema(**user_dict)