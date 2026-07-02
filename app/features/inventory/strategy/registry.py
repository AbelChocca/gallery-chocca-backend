from app.features.inventory.types import (
    InventoryMovementType
)

from app.features.inventory.strategy.base import InventoryMovementStrategy

from app.features.inventory.strategy.entry import (
    EntryStrategy
)
from app.features.inventory.strategy.sale import (
    SaleStrategy
)
from app.features.inventory.strategy.customer_return_strategy import CustomerReturnStrategy
from app.features.inventory.strategy.supplier_return_strategy import SupplierReturnStrategy
from app.features.inventory.strategy.adjustment import (
    ManualAdjustmentStrategy
)

inventory_movement_registry = {
    InventoryMovementType.ENTRY:
        EntryStrategy(),

    InventoryMovementType.CUSTOMER_RETURN:
        CustomerReturnStrategy(),

    InventoryMovementType.SALE:
        SaleStrategy(),

    InventoryMovementType.SUPPLIER_RETURN:
        SupplierReturnStrategy(),

    InventoryMovementType.MANUAL_ADJUSTMENT:
        ManualAdjustmentStrategy(),
}

def get_inventory_strategy(
    movement_type: InventoryMovementType
) -> InventoryMovementStrategy:

    return inventory_movement_registry[
        movement_type
    ]