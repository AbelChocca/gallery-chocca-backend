from typing import Dict, Any
from app.core.exceptions import ValidationError

class VariantSize:
    def __init__(
            self,
            size: str,
            id: int|None = None,
            sku: str | None = None,
            variant_id: int|None = None,
            barcode: str | None = None
            ):
        

        self.id: int|None = id
        self.variant_id: int|None = variant_id
        self.size: str = size
        self.sku = sku

        self.barcode = barcode

    @property
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "variant_id": self.variant_id,
            "size": self.size,
        }
    
    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "VariantSize":
        return cls(
            id=data["id"],
            variant_id=data["variant_id"],
            size=data["size"],
        )
    
    def assign_sku(self, product_name: str, variant_color: str):
        variant_sku = ''.join(s[0].upper() for s in product_name.split(' '))
        variant_sku += '-' + variant_color[0:3].upper()
        variant_sku += '-' + self.size.upper()

        self.sku = variant_sku
    
    def restock(self, quantity: int) -> None:
        if (self._stock + quantity) < 0:
            raise ValidationError(
                f"Cannot restock variant {self.id}",
                {
                    "current_stock": self._stock,
                    "quantity_to_restock": quantity
                }
            )
        self._stock += quantity

    def __str__(self):
        return f"Size: {self.size}"