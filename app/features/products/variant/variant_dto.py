from app.features.media.dto import UpdateImageCommand
from app.features.products.variant_size.variant_size_dto import UpdateVariantSizeCommand, PublishVariantSizeCommand, VariantSizeDTO
from app.features.media.dto import ReadMediaImageDTO

from dataclasses import dataclass, field
from typing import List

@dataclass(slots=True)
class ProductVariantDTO:
    id: int | None
    product_id: int | None

    color: str

    sizes: list[VariantSizeDTO] = field(default_factory=list)
    imagenes: list[ReadMediaImageDTO] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "product_id": self.product_id,
            "color": self.color,
            "sizes": [
                size.to_dict()
                for size in self.sizes
            ],
            "imagenes": [
                image.to_dict()
                for image in self.imagenes
            ],
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> "ProductVariantDTO":

        return cls(
            id=data["id"],
            product_id=data.get("product_id"),
            color=data["color"],
            sizes=[
                VariantSizeDTO.from_dict(size)
                for size in data["sizes"]
            ],
            imagenes=[
                ReadMediaImageDTO.from_dict(image)
                for image in data["imagenes"]
            ],
        )

@dataclass(slots=True)
class GridProductVariantDTO:
    id: int

    imagenes: list[ReadMediaImageDTO] = field(default_factory=list)

    def to_dict(self):
        return {
            "id": self.id,
            "imagenes": [
                image.to_dict()
                for image in self.imagenes
            ],
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> "GridProductVariantDTO":

        return cls(
            id=data["id"],
            imagenes=[
                ReadMediaImageDTO.from_dict(image)
                for image in data["imagenes"]
            ],
        )

@dataclass
class UpdateProductVariantCommand:
    id: int | None = None
    product_id: int | None = None
    color: str | None = None
    sizes: List[UpdateVariantSizeCommand] | None = None
    imagenes: List[UpdateImageCommand] | None = None
    temp_key: str | None = None

    # flags
    to_delete: bool = False

@dataclass
class PublishProductVariantCommand:
    color: str
    sizes: List[PublishVariantSizeCommand]

    temp_key: str