from app.features.inventory.strategy.base import InventoryMovementStrategy
from app.core.exceptions import InvalidOperation

class EntryStrategy(
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
                "Entry quantity must be positive.",
                {
                    "quantity": quantity
                }
            )

        return current_stock + quantity