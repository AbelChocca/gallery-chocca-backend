from app.core.authorization.permissions import Permission
from app.features.user.types import UserRole
from app.core.authorization.role_permissions import ROLE_PERMISSIONS

def has_permission(
    role: UserRole,
    permission: Permission,
) -> bool:
    return permission in ROLE_PERMISSIONS.get(role, set())