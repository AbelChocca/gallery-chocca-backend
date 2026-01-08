from typing import List, Optional, Union, Dict

from app.domain.media.entities.image import ImageEntity
from app.domain.product.exceptions.variant_exception import MissingSizesException, ColorTooShortException, CannotDeleteVariantImage

class ProductVariant:
    def __init__(
            self,
            color: str,
            tallas: List[str],
            id: Optional[int] = None,
            product_id: Optional[int] = None
            ):
        self._validate_variant(
            color=color,
            tallas=tallas
        )
        
        self.id = id
        self.product_id = product_id
        self.color = color
        self.tallas = tallas
        self.imagenes: List[ImageEntity] = []

    def agregar_image(
            self, 
            new_image: ImageEntity
            ) -> None:
        if self.id is not None:
            new_image.set_id(self.id)
        self.imagenes.append(new_image)

    def get_all_images_public_id(self) -> List[str]:
        return [image.service_id for image in self.imagenes]
    
    def get_images(self) -> List[ImageEntity]:
        return self.imagenes

    def update_variant(
            self,
            color: Optional[str] = None,
            tallas: Optional[List[str]] = None
            ):
        self.color = color if color is not None else self.color
        self.tallas = tallas if tallas is not None else self.tallas

    def sync_images_id(
        self,
        services_id: Dict[str, int]
    ) -> None:
        for image in self.imagenes:
            if image.service_id in services_id:
                image.set_id(services_id[image.service_id])
         
    def raise_cannot_delete_image(self, images_id_to_delete: List[Union[str, None]]) -> None:
        diff: int = len(self.imagenes) - len(images_id_to_delete)

        if diff < 1:
            raise CannotDeleteVariantImage(f"Variant: {self.id} must be at least one image, cannot delete")

    @staticmethod
    def _validate_variant(
        color: str,
        tallas: List[str],
    )->None:
        if len(color) < 4:
            raise ColorTooShortException()
        if not tallas:
            raise MissingSizesException()
