from app.features.inventory.services.inventory_service import InventoryService
from app.features.media.service import MediaService
from app.features.media.types import ImageType
from app.features.inventory.dtos.inventory import ProductInventoryRowDTO
from app.shared.pagination.pagination_service import PaginationService
from app.shared.pagination.dto import PaginatedDTO
from app.core.constants.color_families import COLOR_FAMILY_MAP

class GetInventoryProductsUseCase:

    def __init__(
        self,
        inventory_service: InventoryService,
        media_service: MediaService,
        pagination_service: PaginationService
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
        color: str | None = None,
        size: str | None = None,
        current_location_id: int,
    ) -> PaginatedDTO[ProductInventoryRowDTO]:
        
        offset = self._pagination_service.get_offset(page, limit)

        current_page = self._pagination_service.get_current_page(offset, limit)

        colors = None
        
        if color:
            colors = COLOR_FAMILY_MAP[color]

        total_items = await self._inventory_service.get_inventory_products_count(
            search=search,
            colors=colors,
            size=size
        )

        inventory_rows = await (
            self._inventory_service.get_inventory_products(
                offset=offset,
                limit=limit,
                search=search,
                colors=colors,
                size=size,
                current_location_id=current_location_id,
            )
        )


        variants_id = [
            row.variant_id
            for row in inventory_rows
        ]


        images_by_variant = await (
            self._media_service.get_first_images_by_owner_ids(
                owner_type=ImageType.variant,
                owner_ids=variants_id,
            )
        )

        for row in inventory_rows:
            image = images_by_variant.get(
                row.variant_id
            )

            if image:
                row.image_url = image.image_url

        total_pages = self._pagination_service.get_total_pages(total_items, limit)

        return PaginatedDTO.create(
            items=inventory_rows,
            total_items=total_items,
            current_page=current_page,
            total_pages=total_pages,
        )