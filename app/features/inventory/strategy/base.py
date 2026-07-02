from abc import ABC, abstractmethod

class InventoryMovementStrategy(ABC):

    @abstractmethod
    def compute_new_stock(
        self,
        *,
        current_stock: int,
        quantity: int
    ) -> int:
        pass