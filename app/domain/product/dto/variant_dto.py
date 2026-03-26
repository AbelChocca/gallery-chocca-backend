from dataclasses import dataclass
from typing import List

from app.domain.media.media_dto import UpdateImageCommand
from app.domain.product.dto.variant_size_dto import UpdateVariantSizeCommand, PublishVariantSizeCommand

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
    
    @property
    def new_sizes_count(self) -> int:
        return sum(
            1
            for size in (self.sizes or [])
            if size.id is None
        )
    
    @property
    def existing_images_count(self) -> int:
        return sum(
            1
            for image in (self.imagenes or [])
            if image.id is not None
        )
    
    @property
    def existing_sizes_count(self) -> int:
        return sum(
            1
            for size in (self.sizes or [])
            if size.id is not None
        )
    
    @property
    def images_to_delete_count(self) -> int:
        return sum(
            1
            for image in (self.imagenes or [])
            if image.id is not None and image.to_delete
        )
    
    @property
    def sizes_to_delete_count(self) -> int:
        return sum(
            1
            for size in (self.sizes or [])
            if size.id is not None and size.to_delete
        )

@dataclass
class PublishProductVariantCommand:
    color: str
    sizes: List[PublishVariantSizeCommand]

    temp_key: str