from app.core.authorization.permissions import Permission
from app.features.user.types import UserRole

ROLE_PERMISSIONS = {

    UserRole.ADMIN: [
        *list(Permission)
    ],

    UserRole.MANAGER: [
        Permission.MATERIAL_READ,
        Permission.MATERIAL_CREATE,
        Permission.MATERIAL_UPDATE,

        Permission.INVENTORY_READ,
        Permission.INVENTORY_CREATE,

        Permission.PRODUCT_READ,
        Permission.PRODUCT_CREATE,
        Permission.PRODUCT_UPDATE,

        Permission.SLIDE_READ,
        Permission.SLIDE_CREATE,
        Permission.SLIDE_UPDATE,

        Permission.PRICING_READ,
        Permission.PRICING_UPDATE,

        Permission.REPORT_VIEW,
        Permission.DASHBOARD_READ
    ],

    UserRole.INVENTORY: [
        Permission.MATERIAL_READ,
        Permission.MATERIAL_CREATE,
        Permission.MATERIAL_UPDATE,
        Permission.MATERIAL_DELETE,

        Permission.INVENTORY_READ,
        Permission.INVENTORY_CREATE,
        Permission.INVENTORY_UPDATE,

        Permission.PRODUCT_READ,
        Permission.PRODUCT_CREATE,
        Permission.PRODUCT_UPDATE,

        Permission.REPORT_VIEW,
        Permission.REPORT_EXPORT,
         Permission.DASHBOARD_READ
    ],

    UserRole.SELLER: [
        Permission.PRODUCT_READ,
        Permission.MATERIAL_READ,
        Permission.INVENTORY_READ,
        Permission.DASHBOARD_READ
    ],

    UserRole.ACCOUNTANT: [
        Permission.MATERIAL_READ,
        Permission.MATERIAL_CREATE,
        Permission.MATERIAL_UPDATE,
        Permission.MATERIAL_DELETE,

        Permission.INVENTORY_READ,
        Permission.INVENTORY_CREATE,
        Permission.INVENTORY_UPDATE,
        Permission.REPORT_VIEW,
        Permission.REPORT_EXPORT,
        Permission.DASHBOARD_READ
    ],

    UserRole.USER: list(),
}