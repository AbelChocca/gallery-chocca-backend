from datetime import datetime, timezone

from app.features.inventory.types import (
    InventoryMovementType,
    InventoryOwnerType
)


class InventoryMovement:
    def __init__(
        self,
        owner_type: InventoryOwnerType,
        owner_id: int,
        owner_name: str,
        owner_code: str,
        type: InventoryMovementType,
        quantity: int,
        previous_stock: int,
        new_stock: int,
        reason: str | None = None,
        id: int | None = None,
        created_at: datetime | None = None
    ):
        self._id = id

        self.owner_type = owner_type
        self.owner_id = owner_id
        self.owner_name = owner_name
        self.owner_code = owner_code

        self.type = type
        self.quantity = quantity

        self.previous_stock = previous_stock
        self.new_stock = new_stock

        self.reason = reason

        self.created_at = (
            created_at
            or datetime.now(timezone.utc)
        )

    @property
    def id(self) -> int | None:
        return self._id

    @property
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "owner_type": self.owner_type,
            "owner_id": self.owner_id,
            "owner_name": self.owner_name,
            "owner_code": self.owner_code,
            "type": self.type,
            "quantity": self.quantity,
            "previous_stock": self.previous_stock,
            "new_stock": self.new_stock,
            "reason": self.reason,
            "created_at": self.created_at
        }
    
    @classmethod
    def create(
        cls,
        owner_type: InventoryOwnerType,
        owner_id: int,
        owner_name: str,
        owner_code: str,
        movement_type: InventoryMovementType,
        quantity: int,
        previous_stock: int,
        new_stock: int,
        reason: str | None = None
    ):
        return cls(
            owner_type=owner_type,
            owner_id=owner_id,
            owner_code=owner_code,
            owner_name=owner_name,
            type=movement_type,
            quantity=quantity,
            previous_stock=previous_stock,
            new_stock=new_stock,
            reason=reason
        )