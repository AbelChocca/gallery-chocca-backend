from app.features.inventory.strategy.base import InventoryMovementStrategy
from app.core.exceptions import InvalidOperation

class SaleStrategy(
    InventoryMovementStrategy
):

    def compute_new_stock(
        self,
        *,
        current_stock: int,
        quantity: int
    ) -> int:

        if quantity <= 0:
            raise InvalidOperation(
                "Sale quantity must be positive.",
                {
                    "quantity": quantity
                }
            )

        if current_stock < quantity:
            raise InvalidOperation(
                "Insufficient stock.",
                {
                    "current_stock": current_stock,
                    "quantity": quantity
                }
            )

        return current_stock - quantity