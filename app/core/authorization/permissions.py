from enum import StrEnum

class Permission(StrEnum):

    DASHBOARD_READ = "dashboard:read"

    # Materiales
    MATERIAL_READ = "material:read"
    MATERIAL_CREATE = "material:create"
    MATERIAL_UPDATE = "material:update"
    MATERIAL_DELETE = "material:delete"

    # Inventario
    INVENTORY_READ = "inventory:read"
    INVENTORY_CREATE = "inventory:create"
    INVENTORY_UPDATE = "inventory:update"

    # Usuarios
    USER_READ = "user:read"
    USER_CREATE = "user:create"
    USER_UPDATE = "user:update"
    USER_DELETE = "user:delete"

    # Reportes
    REPORT_VIEW = "report:view"
    REPORT_EXPORT = "report:export"

    # Productos
    PRODUCT_READ = "product:read"
    PRODUCT_CREATE = "product:create"
    PRODUCT_UPDATE = "product:update"
    PRODUCT_DELETE = "product:delete"

    # Slides / Banner / Hero
    SLIDE_READ = "slide:read"
    SLIDE_CREATE = "slide:create"
    SLIDE_UPDATE = "slide:update"
    SLIDE_DELETE = "slide:delete"

    # Pricing / Precios / Planes
    PRICING_READ = "pricing:read"
    PRICING_CREATE = "pricing:create"
    PRICING_UPDATE = "pricing:update"
    PRICING_DELETE = "pricing:delete"