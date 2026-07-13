from app.features.inventory.strategy.base import InventoryMovementStrategy
from app.core.exceptions import InvalidOperation
from decimal import Decimal

class ManualAdjustmentStrategy(
    InventoryMovementStrategy
):

    def compute_new_stock(
        self,
        *,
        current_stock: Decimal,
        quantity: Decimal
    ) -> Decimal:

        if quantity < Decimal("0"):
            raise InvalidOperation(
                "Stock must be >= 0 after adjustment.",
                {
                    "current_stock": current_stock,
                    "quantity": quantity
                }
            )

        return quantity