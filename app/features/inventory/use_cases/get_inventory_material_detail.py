from app.features.inventory.services.inventory_service import (
    InventoryService,
)

from app.features.material.service import (
    MaterialService,
)

from app.features.media.service import (
    MediaService,
)

from app.features.inventory.dtos.inventory import (
    MaterialInventoryDetailDTO,
)

from app.features.inventory.types.inventory_movement import (
    InventoryOwnerType,
)

from app.features.media.types import (
    ImageType,
)

from app.features.inventory.types.inventory import (
    AvailabilityStatus,
)


class GetInventoryMaterialDetailUseCase:

    def __init__(
        self,
        inventory_service: InventoryService,
        material_service: MaterialService,
        media_service: MediaService,
    ) -> None:

        self._inventory_service = inventory_service
        self._material_service = material_service
        self._media_service = media_service


    async def execute(
        self,
        *,
        material_id: int,
    ) -> MaterialInventoryDetailDTO:


        inventory_detail = await (
            self._inventory_service
            .get_inventory_material_detail(
                material_id=material_id,
            )
        )


        locations = await (
            self._inventory_service
            .get_owner_inventory_locations(
                owner_type=InventoryOwnerType.MATERIAL,
                owner_id=material_id,
            )
        )

        inventory_detail.locations = locations


        inventory_detail.components = await (
            self._material_service
            .get_components(
                material_id=material_id,
            )
        )


        image = await (
            self._media_service
            .get_first_image_by_owner(
                owner_type=ImageType.material,
                owner_id=material_id,
            )
        )


        if image:
            inventory_detail.image_url = (
                image.image_url
            )


        return inventory_detail



    def _calculate_status(
        self,
        available_quantity,
        minimum_stock,
    ) -> AvailabilityStatus:

        if available_quantity <= 0:
            return AvailabilityStatus.OUT_OF_STOCK


        if available_quantity <= minimum_stock:
            return AvailabilityStatus.CRITICAL


        return AvailabilityStatus.AVAILABLE