from app.features.inventory.strategy.base import InventoryMovementStrategy
from app.core.exceptions import InvalidOperation

class ManualAdjustmentStrategy(
    InventoryMovementStrategy
):

    def compute_new_stock(
        self,
        *,
        current_stock: int,
        quantity: int
    ) -> int:

        if quantity < 0:
            raise InvalidOperation(
                "Stock must be >= 0 after adjustment.",
                {
                    "current_stock": current_stock,
                    "quantity": quantity
                }
            )

        return quantity