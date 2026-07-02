from dataclasses import dataclass
from datetime import datetime

from app.features.inventory.types import InventoryMovementType, InventoryOwnerType
from app.features.inventory.inventory_movement_entity import InventoryMovement
from app.shared.pagination.dto import PaginatedDTO, PaginationDTO

@dataclass(slots=True)
class InventoryMovementDTO:
    id: int
    owner_id: int
    owner_type: InventoryOwnerType
    owner_name: str
    owner_code: str
    type: InventoryMovementType
    quantity: int
    previous_stock: int
    new_stock: int
    created_at: str
    reason: str | None = None

    @classmethod
    def from_entity(
        cls,
        movement: InventoryMovement
    ) -> "InventoryMovementDTO":
        return cls(
            id=movement.id,
            owner_id=movement.owner_id,
            owner_type=movement.owner_type,
            type=movement.type,
            owner_name=movement.owner_name,
            owner_code=movement.owner_code,
            quantity=movement.quantity,
            previous_stock=movement.previous_stock,
            new_stock=movement.new_stock,
            reason=movement.reason,
            created_at=movement.created_at.isoformat()
        )
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "owner_id": self.owner_id,
            "owner_type": self.owner_type.value,
            "owner_name": self.owner_name,
            "owner_code": self.owner_code,
            "type": self.type.value,
            "quantity": self.quantity,
            "previous_stock": self.previous_stock,
            "new_stock": self.new_stock,
            "reason": self.reason,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(
        cls,
        data: dict
    ) -> "InventoryMovementDTO":
        return cls(
            id=data["id"],
            owner_id=data["owner_id"],
            owner_type=InventoryOwnerType(
                data["owner_type"]
            ),
            owner_name=data['owner_name'],
            owner_code=data['owner_code'],
            type=InventoryMovementType(
                data["type"]
            ),
            quantity=data["quantity"],
            previous_stock=data["previous_stock"],
            new_stock=data["new_stock"],
            reason=data["reason"],
            created_at=data["created_at"]
        )
    
class InventoryMovementPaginatedDTO(
    PaginatedDTO[InventoryMovementDTO]
):

    def to_dict(self) -> dict:
        return {
            "items": [
                item.to_dict()
                for item in self.items
            ],
            "total_items": self.total_items,
            "pagination": {
                "current_page": self.pagination.current_page,
                "total_pages": self.pagination.total_pages
            }
        }

    @classmethod
    def from_dict(
        cls,
        data: dict
    ) -> "InventoryMovementPaginatedDTO":
        return cls(
            items=[
                InventoryMovementDTO.from_dict(item)
                for item in data["items"]
            ],
            total_items=data["total_items"],
            pagination=PaginationDTO(
                current_page=data["pagination"]["current_page"],
                total_pages=data["pagination"]["total_pages"]
            )
        )

@dataclass
class CreateMovementCommand:
    owner_id: int
    owner_type: InventoryOwnerType
    type: InventoryMovementType
    quantity: int
    reason: str | None = None

@dataclass
class MovementItem:
    owner_id: int
    quantity: int

@dataclass(slots=True)
class UpdatedOwnerStockResult:
    owner_id: int
    owner_code: str
    owner_name: str
    previous_stock: int
    new_stock: int

@dataclass
class CreateBulkMovementCommand:
    owner_type: InventoryOwnerType
    type: InventoryMovementType
    items: list[MovementItem]
    reason: str | None = None

    def get_material_ids(self) -> list[int]:
        return list(
            dict.fromkeys(
                item.owner_id
                for item in self.items
            )
        )
    
    def get_quantities_by_owner_id(self) -> dict[int, int]:
        quantities: dict[int, int] = {}

        for item in self.items:
            if item.owner_id in quantities:
                quantities[item.owner_id] += item.quantity
            else:
                quantities[item.owner_id] = item.quantity

        return quantities

@dataclass(slots=True)
class InventoryOwnerDTO:
    id: int
    code: str
    name: str
    stock: int

@dataclass(slots=True)
class InventoryMovementAdminDTO:
    id: int

    owner_id: int
    owner_type: InventoryOwnerType

    owner_code: str
    owner_name: str

    type: InventoryMovementType

    quantity: int
    previous_stock: int
    new_stock: int

    created_at: str
    reason: str | None = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "owner_id": self.owner_id,
            "owner_type": self.owner_type.value,
            "owner_code": self.owner_code,
            "owner_name": self.owner_name,
            "type": self.type.value,
            "quantity": self.quantity,
            "previous_stock": self.previous_stock,
            "new_stock": self.new_stock,
            "reason": self.reason,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(
        cls,
        data: dict
    ) -> "InventoryMovementAdminDTO":
        return cls(
            id=data["id"],
            owner_id=data["owner_id"],
            owner_type=InventoryOwnerType(
                data["owner_type"]
            ),
            owner_code=data["owner_code"],
            owner_name=data["owner_name"],
            type=InventoryMovementType(
                data["type"]
            ),
            quantity=data["quantity"],
            previous_stock=data["previous_stock"],
            new_stock=data["new_stock"],
            reason=data["reason"],
            created_at=data["created_at"]
        )

@dataclass(slots=True)
class InventoryMovementAdminPaginatedDTO(
    PaginatedDTO[InventoryMovementAdminDTO]
):

    def to_dict(self) -> dict:
        return {
            "items": [
                item.to_dict()
                for item in self.items
            ],
            "total_items": self.total_items,
            "pagination": {
                "current_page": self.pagination.current_page,
                "total_pages": self.pagination.total_pages
            }
        }

    @classmethod
    def from_dict(
        cls,
        data: dict
    ) -> "InventoryMovementAdminPaginatedDTO":
        return cls(
            items=[
                InventoryMovementAdminDTO.from_dict(item)
                for item in data["items"]
            ],
            total_items=data["total_items"],
            pagination=PaginationDTO(
                current_page=data["pagination"]["current_page"],
                total_pages=data["pagination"]["total_pages"]
            )
        )

from dataclasses import dataclass
from datetime import datetime

from app.features.inventory.types import InventoryMovementType, InventoryOwnerType


@dataclass(slots=True)
class InventoryMovementFilters:
    owner_id: int | None = None
    owner_type: InventoryOwnerType | None = None

    type: InventoryMovementType | None = None
    from_date: datetime | None = None
    to_date: datetime | None = None
    search: str | None = None

    def to_dict(self) -> dict:
        return {
            "owner_id": self.owner_id,
            "owner_type": (
                self.owner_type.value
                if self.owner_type
                else None
            ),
            "type": self.type.value if self.type else None,
            "from_date": (
                self.from_date.isoformat()
                if self.from_date
                else None
            ),
            "to_date": (
                self.to_date.isoformat()
                if self.to_date
                else None
            ),
            "search": self.search,
        }