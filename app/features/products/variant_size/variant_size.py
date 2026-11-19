import secrets
import string
from uuid import uuid4


from typing import Dict, Any
from app.core.exceptions import ValidationError

class VariantSize:
    BARCODE_PREFIX = "GC"
    BARCODE_LENGTH = 12
    BARCODE_ALPHABET = string.ascii_uppercase + string.digits

    def __init__(
        self,
        size: str,
        id: int | None = None,
        sku: str | None = None,
        variant_id: int | None = None,
        barcode: str | None = None,
    ):
        self.id = id
        self.variant_id = variant_id
        self.size = size
        self.sku = sku

        self.barcode = (
            barcode
            if barcode is not None
            else self.generate_barcode()
        )

    @property
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "variant_id": self.variant_id,
            "size": self.size,
        }

    @staticmethod
    def generate_barcode() -> str:
        suffix = "".join(
            secrets.choice(VariantSize.BARCODE_ALPHABET)
            for _ in range(VariantSize.BARCODE_LENGTH)
        )
        return f"{VariantSize.BARCODE_PREFIX}{suffix}"
    
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
    
    def assign_sku(self, product_name: str, variant_color: str) -> None:
        initials = ''.join(
            word[0].upper()
            for word in product_name.split()
        )

        color = variant_color[:3].upper()
        size = self.size.upper()
        suffix = uuid4().hex[:4].upper()

        self.sku = f"{initials}-{color}-{size}-{suffix}"
    
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