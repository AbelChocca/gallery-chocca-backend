from app.domain.inventory.data_models import InventoryMovementType
from datetime import datetime, timezone

class InventoryMovement:
    def __init__(
            self,
            variant_size_id: int,
            type: InventoryMovementType,
            quantity: int,
            previous_stock: int,
            new_stock: int,
            reason: str | None = None,
            id: int | None = None,
            created_at: datetime | None = None
        ):
        self._id = id
        self.variant_size_id = variant_size_id
        self.type = type
        self.quantity = quantity
        self.previous_stock = previous_stock
        self.new_stock = new_stock
        self.reason = reason
        self.created_at = created_at or datetime.now(timezone.utc)

    @property
    def id(self) -> int:
        return self._id
    
    @property
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "variant_size_id": self.variant_size_id,
            "type": self.type,
            "quantity": self.quantity,
            "previous_stock": self.previous_stock,
            "new_stock": self.new_stock,
            "reason": self.reason,
            "created_at": self.created_at
        }