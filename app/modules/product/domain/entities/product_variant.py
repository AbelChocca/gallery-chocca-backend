from typing import List, Optional

from app.modules.product.domain.entities.variant_image import VariantImage
from app.modules.product.domain.exceptions.variant_exception import MissingSizesException, ColorTooShortException, MissingImagesException

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
            tallas=tallas,
            imagenes=imagenes
        )
        
        self.id = id
        self.product_id = product_id
        self.color = color
        self.tallas = tallas
        self.imagenes = imagenes

    def agregar_image(self, image_url: str, public_id: str) -> None:
        self.imagenes.append(VariantImage(
            url=image_url,
            cloudinary_id=public_id
        ))

    def update_variant(
            self,
            color: Optional[str] = None,
            tallas: Optional[List[str]] = None
            ):
        self.color = color if color is not None else self.color
        self.tallas = tallas if tallas is not None else self.tallas

    @staticmethod
    def _validate_variant(
        color: str,
        tallas: List[str],
        imagenes: List[VariantImage]
    )->None:
        if len(color) < 4:
            raise ColorTooShortException()
        if not tallas:
            raise MissingSizesException()
        if not imagenes:
            raise MissingImagesException()
