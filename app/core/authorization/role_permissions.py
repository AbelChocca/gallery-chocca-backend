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
        Permission.DASHBOARD_READ,
        Permission.BALANCE_READ,
        Permission.BALANCE_CREATE,
        Permission.BALANCE_UPDATE,
        Permission.BALANCE_DELETE,
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
         Permission.DASHBOARD_READ,
        Permission.INVENTORY_LOCATION_READ
    ],

    UserRole.SELLER: [
        Permission.DASHBOARD_READ,

        # Catálogo
        Permission.PRODUCT_READ,
        Permission.PRODUCT_READ,
        Permission.PRODUCT_CREATE,
        Permission.PRODUCT_UPDATE,
        Permission.MATERIAL_READ,

        # Inventario
        Permission.INVENTORY_READ,

        # Pedidos
        Permission.ORDER_READ,
        Permission.ORDER_UPDATE,
        Permission.ORDER_PAYMENT_CREATE,

        # Comprobantes
        Permission.RECEIPT_GENERATE,
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