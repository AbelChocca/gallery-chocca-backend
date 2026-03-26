from typing import List, Dict, Any

from app.domain.media.entities.image import ImageEntity
from app.domain.product.entities.variant_size import VariantSize

from app.domain.product.dto.variant_size_dto import UpdateVariantSizeCommand

from app.core.exceptions import ValidationError


class ProductVariant:
    def __init__(
            self,
            color: str,
            sizes: List[VariantSize] | None = None,
            id: int | None = None,
            product_id: int | None = None
            ):
        self._validate_color(color)

        self.id = id
        self.product_id = product_id
        self.color = color.strip()
        self.sizes = list(sizes) if sizes is not None else []
        self._imagenes: List[ImageEntity] = []

    @property
    def imagenes(self) -> List[ImageEntity]:
        return self._imagenes
    
    @imagenes.setter
    def imagenes(self, new_images: List[ImageEntity]) -> None:
        for image in new_images:
            if not isinstance(image, ImageEntity):
                raise ValidationError(
                    "All images must be ImageEntity",
                    {"entity": "ProductVariant", "event": "imagenes.setter"}
                )
            if image.owner_id is not None and image.owner_id != self.id:
                raise ValidationError(
                    "Image owner id can't be reassigned",
                    {
                        "entity": "ProductVariant",
                        "event": "imagenes.setter"
                    }
                )
            
            if self.id is not None:
                image.owner_id = self.id

        self._imagenes = list(new_images)

    @property
    def images_without_id(self) -> List[ImageEntity]:
        return [image for image in self.imagenes if not image.id]
    
    @property
    def all_images_public_ids(self) -> List[str]:
        return [image.public_id for image in self.imagenes]
    
    @property
    def has_sizes(self) -> bool:
        return len(self.sizes) > 0
    
    @property
    def has_images(self) -> bool:
        return len(self.imagenes) > 0
    
    @property
    def to_dict(self)-> Dict[str, Any]:
        return {
            "id": self.id,
            "product_id": self.product_id,
            "color": self.color,
            "sizes": [
                size.to_dict
                for size in self.sizes
            ],
            "imagenes": [
                image.to_dict
                for image in self.imagenes
            ]
        }

    def agregar_image(
            self, 
            new_image: ImageEntity
            ) -> None:
        if not isinstance(new_image, ImageEntity):
            raise ValidationError(
                "'new_image' must be an ImageEntity",
                {
                    "entity": "ProductVariant",
                    "event": "agregar_image",
                    "new_image_type": type(new_image).__name__
                }
                )
        if not new_image:
            return
        
        if self.id is not None:
            new_image.owner_id = self.id

        self.imagenes.append(new_image)

    def update_variant(
            self,
            *,
            color: str | None = None,
            sizes: list[UpdateVariantSizeCommand] | None = None
            ) -> None:
        if self.id is None:
            return 
        if color is not None:
            self.color = color
        
        if sizes is None:
            return
        
        existing_sizes = {
            size.id: size
            for size in self.sizes
            if size.id is not None
        }
        new_sizes = []

        for size in sizes:
            if size.to_delete: continue

            if size.id is not None and size.id in existing_sizes:
                new_sizes.append(existing_sizes[size.id])
            else:
                new_size = VariantSize(
                    size=size.size,
                )
                new_sizes.append(new_size)
        
        self.sizes = new_sizes

    def add_new_size(
            self,
            size: str
    ) -> None:
        self.sizes.append(
            VariantSize(
                size=size,
                variant_id=self.id or None
            )
        )
        
    def _validate_color(self, v: str) -> None:
        if v is None: return None

        if v.startswith('#'):
            raise ValidationError(
                "Color cannot be hexadecimal tag",
                {"event": "validator/_validate_color", "module": "product_variant"}
            )
        
        if any(char.isdigit() for char in v):
            raise ValidationError(
                "Color can't have any digit",
                {"event": "validator/_validate_color", "module": "product_variant"}
            )
        
        if not v.strip():
            raise ValidationError(
                "Color cannot be empty",
                {"event": "validator/_validate_color", "module": "product_variant"}
            )
        
    def __str__(self):
        res = (
            f"\tColor: {self.color}\n"
        )
        if self.has_sizes:
            res += "\t\t== Sizes ===\n"
            for size in self.sizes:
                res += f"\t\t{size}\n"
        if self.has_images:
            res += "\t\t== Images ==\n"
            for image in self.imagenes:
                res += f"\t\t{image}\n"

        return res
