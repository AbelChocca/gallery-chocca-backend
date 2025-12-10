from typing import List, Optional
from dataclasses import asdict

from app.modules.product.domain.entities.variant_image import VariantImage
from app.shared.exceptions.domain.variant_color_exception import MissingSizesException, ColorTooShortException, MissingImagesException
from app.shared.dto.color_variant_dto import UpdateProductColorVariantDTO, UpdateVariantImageDTO

class VariantColor:
    def __init__(
            self,
            color: str,
            tallas: List[str],
            imagenes: List[VariantImage],
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

    def _update_images(self, new_images: List[UpdateVariantImageDTO]):
        existing_images = {image.id: image for image in self.imagenes}
        for new_img in new_images:
            if not new_img.id in existing_images:
                self.imagenes.append(
                    VariantImage(
                        url=new_img.url,
                        cloudinary_id=new_img.cloudinary_id
                    )
                )

    def update_variant(self, new_variant: UpdateProductColorVariantDTO):
        self._update_images(new_variant.imagenes)

        update = {k: v for k, v in asdict(new_variant).items() if v is not None and k != "imagenes"}
        for k, v in update.items():
            setattr(self, k, v)

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
