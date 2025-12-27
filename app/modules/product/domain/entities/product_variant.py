from typing import List, Optional, Union

from app.modules.product.domain.entities.variant_image import VariantImage
from app.modules.product.domain.exceptions.variant_exception import MissingSizesException, ColorTooShortException, CannotDeleteVariantImage

class ProductVariant:
    def __init__(
            self,
            color: str,
            tallas: List[str],
            imagenes: Optional[List[VariantImage]] = None,
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
        self.imagenes = imagenes if imagenes is not None else []

    def agregar_image(self, image_url: str, public_id: str) -> None:
        self.imagenes.append(VariantImage(
            url=image_url,
            cloudinary_id=public_id
        ))

    def get_all_images_id(self) -> List[str]:
        res: List[str] = []
        for image in self.imagenes:
            res.append(image.cloudinary_id)
        return res

    def update_variant(
            self,
            color: Optional[str] = None,
            tallas: Optional[List[str]] = None
            ):
        self.color = color if color is not None else self.color
        self.tallas = tallas if tallas is not None else self.tallas

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
