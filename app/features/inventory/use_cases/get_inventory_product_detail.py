from app.features.inventory.services.inventory_service import InventoryService
from app.features.inventory.dtos.inventory import ProductInventoryDetailDTO
from app.features.media.service import MediaService
from app.features.media.types import ImageType


class GetInventoryProductDetailUseCase:

    def __init__(
        self,
        inventory_service: InventoryService,
        media_service: MediaService,
    ) -> None:
        self._inventory_service = inventory_service
        self._media_service = media_service


    async def execute(
        self,
        *,
        variant_size_id: int,
    ) -> ProductInventoryDetailDTO:

        inventory_detail = await (
            self._inventory_service
            .get_inventory_product_detail(
                variant_size_id=variant_size_id,
            )
        )


        image = await (
            self._media_service.get_first_image_by_owner(
                owner_type=ImageType.variant,
                owner_id=inventory_detail.variant_id,
            )
        )


        if image:
            inventory_detail.image_url = image.image_url


        return inventory_detail