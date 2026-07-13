from abc import ABC, abstractmethod
from decimal import Decimal

class InventoryMovementStrategy(ABC):

    @abstractmethod
    def compute_new_stock(
        self,
        *,
        current_stock: Decimal,
        quantity: Decimal
    ) -> Decimal:
        pass