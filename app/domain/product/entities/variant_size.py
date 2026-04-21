from typing import Dict, Any
from app.core.exceptions import ValidationError

class VariantSize:
    def __init__(
            self,
            size: str,
            id: int|None = None,
            stock: int | None = None,
            sku: str | None = None,
            variant_id: int|None = None,
            ):
        self.id: int|None = id
        self.variant_id: int|None = variant_id
        self.size: str = size
        self.sku = sku
        self._stock = stock if stock is not None else 0

    @property
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "variant_id": self.variant_id,
            "size": self.size
        }
    
    @property
    def to_inventory_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "size": self.size,
            "stock": self.stock,
            "sku": self.sku
        }
    
    @property
    def stock(self) -> int:
        return self._stock
    
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