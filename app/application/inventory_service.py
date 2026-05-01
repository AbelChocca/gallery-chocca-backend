from app.domain.inventory.data_models import CreateMovementCommand, InventoryMovementFilters
from app.infra.db.repositories.sqlmodel_product_repository import PostgresProductRepository
from app.infra.db.repositories.sqlalchemy_inventory_movement_repo import PostgresInventoryMovementReposity
from app.infra.db.repositories.sqlmodel_image_repository import PostgresImageRepository
from app.infra.cache.protocole import CacheProtocol
from app.domain.inventory.inventory_movement_entity import InventoryMovement
from app.domain.product.dto.product_dto import FilterProductCommand
from app.shared.services.pagination.pagination_service import PaginationService

class InventoryService:
    def __init__(
            self,
            product_repository: PostgresProductRepository,
            inventory_movement_repo: PostgresInventoryMovementReposity,
            image_repository: PostgresImageRepository,
            cache_service: CacheProtocol,
            pagination_service: PaginationService
        ):
        self._product_repository = product_repository
        self._inventory_movement_repo = inventory_movement_repo
        self._image_repository = image_repository
        self._cache_service = cache_service
        self._pagination_service = pagination_service

    async def get_inventory_movements(
        self,
        command: InventoryMovementFilters,
        page: int,
        limit: int
    ) -> dict:
        return await self._cache_service.get_or_set_with_lock(
            tag="inventory_movements",
            callback=self._get_inventory_movements,
            kwargs={
                "filter_command": command,
                "page": page,
                "limit": limit
            },
            key_args={
                "page": page,
                "limit": limit,
                **command.to_dict
            }
        )

    async def create_movement(
        self,
        command: CreateMovementCommand
    ) -> dict:
        variant_size = await self._product_repository.get_variant_size_by_id(command.variant_size_id)
        prev_stock = variant_size.stock
        variant_size.restock(command.quantity)
        
        new_movement = InventoryMovement(
            variant_size_id=command.variant_size_id,
            type=command.type,
            quantity=command.quantity,
            previous_stock=prev_stock,
            new_stock=variant_size.stock,
            reason=command.reason
        )

        await self._inventory_movement_repo.save(new_movement)
        await self._product_repository.save_variant_size(variant_size)

        await self._cache_service.invalidate_entity("product", command.product_id)
        await self._cache_service.invalidate_entities("inventory")
        await self._cache_service.invalidate_entities("inventory_movements")

        return {"message": "Movement registered successfully."}
    
    async def get_inventory_items(
        self,
        filter_command: FilterProductCommand,
        page: int,
        limit: int = 20
    ) -> dict:
        return await self._cache_service.get_or_set_with_lock(
            tag="inventory",
            callback=self._get_inventory_items_data,
            kwargs={
                "filter_command": filter_command,
                "page": page,
                "limit": limit
            },
            key_args={
                "filters": filter_command.to_dict,
                "page": page, 
                "limit": limit
            }
        )
    
    async def _get_inventory_movements(
        self,
        filter_command: InventoryMovementFilters,
        page: int,
        limit: int
    ) -> dict:
        offset = self._pagination_service.get_offset(page, limit)
        movements = await self._inventory_movement_repo.get_with_filters(filter_command, offset, limit)

        total_movements = await self._inventory_movement_repo.count_with_filters(filter_command)

        total_pages = self._pagination_service.get_total_pages(total_movements, limit)
        current_page = self._pagination_service.get_current_page(offset, limit)

        return {
            "movements": [
                movement.to_dict
                for movement in movements
            ],
            "pagination": {
                "total_pages": total_pages,
                "current_page": current_page
            },
            "total_items": total_movements
        }
    
    async def _get_inventory_items_data(
        self,
        filter_command: FilterProductCommand,
        page: int,
        limit: int = 20
    ) -> dict:
        offset = self._pagination_service.get_offset(page, limit)
        products = await self._product_repository.get_inventory_products(
            filter_command=filter_command,
            offset=offset,
            limit=limit
        )

        variant_ids = [variant_id for product in products for variant_id in product.variant_ids]

        image_per_variant_id = await self._image_repository.get_first_image_of_owner_ids(variant_ids)
        for product in products:
            product.sync_images_to_variants(image_per_variant_id)

        total_products = await self._product_repository.count_filtered_products(filter_command)

        total_pages = self._pagination_service.get_total_pages(total=total_products, limit=limit)
        current_page = self._pagination_service.get_current_page(offset=offset, limit=limit)


        return {
            "products": [
                product.to_inventory_dict
                for product in products
            ],
            "pagination": {
                "total_pages": total_pages,
                "current_page": current_page
            },
            "total_items": total_products
        }
