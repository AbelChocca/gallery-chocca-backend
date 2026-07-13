from app.features.inventory.strategy.base import InventoryMovementStrategy
from app.core.exceptions import InvalidOperation

from decimal import Decimal

class SaleStrategy(
    InventoryMovementStrategy
):

    def compute_new_stock(
        self,
        *,
        current_stock: Decimal,
        quantity: Decimal
    ) -> Decimal:

        if quantity <= Decimal("0"):
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