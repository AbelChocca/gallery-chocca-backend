from dataclasses import dataclass

from app.features.inventory.dtos.inventory import CreateInventoryCommand

@dataclass(slots=True)
class VariantSizeDTO:
    id: int | None
    variant_id: int | None

    size: str

    barcode: str | None
    sku: str | None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "variant_id": self.variant_id,
            "size": self.size,
            "barcode": self.barcode,
            "sku": self.sku,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> "VariantSizeDTO":

        return cls(
            id=data["id"],
            variant_id=data["variant_id"],
            size=data["size"],
            barcode=data.get("barcode"),
            sku=data.get("sku"),
        )

@dataclass
class UpdateVariantSizeCommand:
    size: str | None = None
    id: int | None = None
    variant_id: int | None = None

    to_delete: bool = False

@dataclass
class PublishVariantSizeCommand:
    size: str
    
    inventories: list[CreateInventoryCommand]

    barcode: str | None = None