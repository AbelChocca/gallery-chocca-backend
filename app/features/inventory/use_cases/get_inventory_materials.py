from app.features.inventory.services.inventory_service import InventoryService
from app.features.media.service import MediaService
from app.features.media.types import ImageType
from app.features.inventory.dtos.inventory import MaterialInventoryRowDTO
from app.shared.pagination.pagination_service import PaginationService
from app.shared.pagination.dto import PaginatedDTO


class GetInventoryMaterialsUseCase:

    def __init__(
        self,
        inventory_service: InventoryService,
        media_service: MediaService,
        pagination_service: PaginationService,
    ) -> None:
        self._inventory_service = inventory_service
        self._media_service = media_service
        self._pagination_service = pagination_service


    async def execute(
        self,
        *,
        page: int = 0,
        limit: int = 20,
        search: str | None = None,
        material_type=None,
        availability_status=None,
        is_active: bool | None = None,
        current_location_id: int,
    ) -> PaginatedDTO[MaterialInventoryRowDTO]:

        offset = self._pagination_service.get_offset(
            page,
            limit,
        )

        current_page = self._pagination_service.get_current_page(
            offset,
            limit,
        )


        total_items = await (
            self._inventory_service
            .get_inventory_materials_count(
                current_location_id=current_location_id,
                search=search,
                material_type=material_type,
                availability_status=availability_status,
                is_active=is_active,
            )
        )


        inventory_rows = await (
            self._inventory_service
            .get_inventory_materials(
                current_location_id=current_location_id,

                offset=offset,
                limit=limit,

                search=search,
                material_type=material_type,
                availability_status=availability_status,
                is_active=is_active,
            )
        )


        materials_id = [
            row.material_id
            for row in inventory_rows
        ]

        images_by_material = await (
            self._media_service
            .get_first_images_by_owner_ids(
                owner_type=ImageType.material,
                owner_ids=materials_id,
            )
        )


        for row in inventory_rows:
            image = images_by_material.get(
                row.material_id
            )

            if image:
                row.image_url = image.image_url


        total_pages = (
            self._pagination_service
            .get_total_pages(
                total_items,
                limit,
            )
        )


        return PaginatedDTO.create(
            items=inventory_rows,

            total_items=total_items,

            current_page=current_page,

            total_pages=total_pages,
        )