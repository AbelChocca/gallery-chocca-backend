from app.features.media.service import MediaService
from app.features.products.product import Product
from app.features.media.types import ImageType

class ProductEnricher:

    def __init__(
        self,
        media_service: MediaService,
    ):
        self._media_service = media_service


    async def attach_variant_images(
        self,
        products: list[Product],
    ) -> None:

        variant_ids = []

        for product in products:
            variant_ids.extend(
                product.variant_ids
            )

        if not variant_ids:
            return

        images = await self._media_service.get_by_owners(
            owner_type=ImageType.variant,
            owner_ids=variant_ids
        )

        images_by_owner = (
            self._media_service.group_images_by_owner(
                images
            )
        )

        for product in products:
            for variant in product.variants:
                variant.imagenes = images_by_owner.get(
                    variant.id,
                    [],
                )