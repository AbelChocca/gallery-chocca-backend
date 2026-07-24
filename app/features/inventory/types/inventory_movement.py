from enum import Enum

class InventoryMovementType(str, Enum):
    ENTRY = "ENTRY"
    MANUAL_ADJUSTMENT = "MANUAL_ADJUSTMENT"
    USAGE = "USAGE"
    SALE = "SALE"
    CUSTOMER_RETURN = "CUSTOMER_RETURN"
    SUPPLIER_RETURN = "SUPPLIER_RETURN"
    TRANSFER = "TRANSFER"

class InventoryOwnerType(str, Enum):
    PRODUCT = "PRODUCT"
    MATERIAL = "MATERIAL"