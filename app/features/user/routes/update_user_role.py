from typing import Annotated

from fastapi import Depends, Path, Body, status

from app.features.user.dependency import get_user_service
from app.features.user.service import UserService
from app.features.user.user_route import router
from app.features.user.user_schema import UpdateUserRoleSchema
from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission

@router.patch(
    "/{user_id}/role",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update user role",
    dependencies=[
        require_permission(Permission.USER_UPDATE)
    ]
)
async def update_user_role(
    user_id: Annotated[int, Path(...)],
    body: Annotated[UpdateUserRoleSchema, Body(...)],
    service: Annotated[UserService, Depends(get_user_service)],
) -> None:
    await service.update_role_by_user_id(
        user_id=user_id,
        role=body.role,
    )