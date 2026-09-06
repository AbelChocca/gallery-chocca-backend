from datetime import datetime, timezone
from decimal import Decimal

from app.features.inventory.types.inventory_movement import (
    InventoryMovementType,
    InventoryOwnerType,
)
from app.features.inventory.types.inventory_reference import (
    InventoryReferenceType,
)


class InventoryMovement:

    def __init__(
        self,
        *,
        owner_type: InventoryOwnerType,
        owner_id: int,
        owner_name: str,
        owner_code: str,

        location_id: int,

        type: InventoryMovementType,

        quantity: Decimal,
        previous_stock: Decimal,
        new_stock: Decimal,

        reference_type: InventoryReferenceType | None = None,
        reference_id: int | None = None,

        performed_by: int | None = None,

        reason: str | None = None,

        id: int | None = None,
        created_at: datetime | None = None,
    ) -> None:

        self.id = id

        self.owner_type = owner_type
        self.owner_id = owner_id
        self.owner_name = owner_name
        self.owner_code = owner_code

        self.location_id = location_id

        self.type = type

        self.quantity = quantity
        self.previous_stock = previous_stock
        self.new_stock = new_stock

        self.reference_type = reference_type
        self.reference_id = reference_id

        self.performed_by = performed_by

        self.reason = reason

        self.created_at = (
            created_at
            if created_at is not None
            else datetime.now(timezone.utc)
        )

    @property
    def to_dict(self) -> dict:
        return {
            "id": self.id,

            "owner_type": self.owner_type,
            "owner_id": self.owner_id,
            "owner_name": self.owner_name,
            "owner_code": self.owner_code,

            "location_id": self.location_id,

            "type": self.type,

            "quantity": str(self.quantity),
            "previous_stock": str(self.previous_stock),
            "new_stock": str(self.new_stock),

            "reference_type": self.reference_type,
            "reference_id": self.reference_id,

            "performed_by": self.performed_by,

            "reason": self.reason,

            "created_at": self.created_at,
        }

    @classmethod
    def create(
        cls,
        *,
        owner_type: InventoryOwnerType,
        owner_id: int,
        owner_name: str,
        owner_code: str,

        location_id: int,

        movement_type: InventoryMovementType,

        quantity: Decimal,
        previous_stock: Decimal,
        new_stock: Decimal,

        reference_type: InventoryReferenceType | None = None,
        reference_id: int | None = None,

        performed_by: int | None = None,

        reason: str | None = None,
    ) -> "InventoryMovement":

        return cls(
            owner_type=owner_type,
            owner_id=owner_id,
            owner_name=owner_name,
            owner_code=owner_code,

            location_id=location_id,

            type=movement_type,

            quantity=quantity,
            previous_stock=previous_stock,
            new_stock=new_stock,

            reference_type=reference_type,
            reference_id=reference_id,

            performed_by=performed_by,

            reason=reason,
        )