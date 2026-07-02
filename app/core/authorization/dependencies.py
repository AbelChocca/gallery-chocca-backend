from typing import Callable

from fastapi import Depends

from app.api.security.resolvers.sessions import get_user_session
from app.core.authorization.permissions import Permission
from app.core.authorization.resolver import has_permission
from app.api.security.exceptions import SecurityException
from app.features.auth.schema import ReadSessionSchema

def require_permission(permission: Permission):
    def dependency(
        current_user: ReadSessionSchema = Depends(get_user_session),
    ):
        if not has_permission(
            current_user.role,
            permission,
        ):
            raise SecurityException(
                message="User attempted to access a resource without the required permission.",
                context={
                    "user_id": current_user.id,
                    "role": current_user.role,
                    "required_permission": permission.value,
                },
            )

        return current_user

    return Depends(dependency)


def require_any_permission(
    *permissions: Permission,
) -> Callable:
    def dependency(
        current_user: ReadSessionSchema = Depends(get_user_session),
    ):
        if not any(
            has_permission(
                current_user.role,
                permission,
            )
            for permission in permissions
        ):
            raise SecurityException(
                message="User attempted to access a resource without any of the required permissions.",
                context={
                    "user_id": current_user.id,
                    "role": current_user.role,
                    "required_permissions": [permission.value for permission in permissions],
                    "authorization_mode": "any",
                },
            )

        return current_user

    return Depends(dependency)


def require_all_permissions(
    *permissions: Permission,
) -> Callable:
    def dependency(
        current_user: ReadSessionSchema = Depends(get_user_session),
    ):
        if not all(
            has_permission(
                current_user.role,
                permission,
            )
            for permission in permissions
        ):
            raise SecurityException(
                message="User attempted to access a resource without all of the required permissions.",
                context={
                    "user_id": current_user.id,
                    "role": current_user.role,
                    "required_permissions": [permission.value for permission in permissions],
                    "authorization_mode": "all",
                },
            )

        return current_user

    return Depends(dependency)