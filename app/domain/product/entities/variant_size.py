from typing import Dict, Any

class VariantSize:
    def __init__(
            self,
            size: str,
            id: int|None = None,
            variant_id: int|None = None,
            ):
        self.id: int|None = id
        self.variant_id: int|None = variant_id
        self.size: str = size

    @property
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "variant_id": self.variant_id,
            "size": self.size
        }

    def __str__(self):
        return f"Size: {self.size}"