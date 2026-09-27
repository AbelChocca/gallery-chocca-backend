# Script ejecutado el 24 de julio del 2026
# NO EJECUTAR ESTE SCRIPT POR EL MOMENTO


import asyncio
import random

from app.infra.db.config import async_session_factory
from app.infra.db.uow.unit_of_work import UnitOfWork

from app.features.inventory.services.inventory_service import (
    InventoryService,
)

from app.features.inventory.services.inventory_movement_service import (
    InventoryMovementService,
)
from app.features.inventory.repositories.inventory_repository import InventoryRepository

from app.features.inventory.types.inventory_movement import (
    InventoryOwnerType,
)

from app.features.inventory.types.inventory_reference import InventoryReferenceType

from app.features.inventory.types.inventory_movement import InventoryMovementType

from app.shared.pagination.pagination_service import PaginationService


LOCATION_ID = 1

InventoryRepository.get_owner_inventories

class VariantSizeInventoryMigration:

    def __init__(
        self,
        *,
        inventory_repository: InventoryRepository,
        inventory_service: InventoryService,
        inventory_movement_service: InventoryMovementService,
        location_id: int,
    ) -> None:

        self._inventory_repository = inventory_repository

        self._inventory_service = inventory_service

        self._inventory_movement_service = (
            inventory_movement_service
        )

        self._location_id = location_id


    async def execute(self) -> None:

        variant_sizes = (
            await self._inventory_service.get_inventory_products(
                limit=100000,
                current_location_id=self._location_id
            )
        )

        print(
            f"Found {len(variant_sizes)} variant sizes."
        )


        for index, variant_size in enumerate(
            variant_sizes,
            start=1,
        ):

            print(
                f"[{index}/{len(variant_sizes)}] "
                f"Creating inventory SKU '{variant_size.sku}'..."
            )

            await self._create_inventory(
                variant_size
            )


        print(
            "Variant size inventory migration completed successfully."
        )


    async def _create_inventory(
        self,
        variant_size,
    ) -> None:


        inventories = await self._inventory_repository.get_owner_inventories(
            owner_id=variant_size.variant_size_id,
            owner_type=InventoryOwnerType.PRODUCT
        )

        if inventories:
            return

        initial_stock = random.randint(5, 250)

        movement_type = random.choice(
            [
                InventoryMovementType.MANUAL_ADJUSTMENT,
                InventoryMovementType.ENTRY,
            ]
        )

        minimum_stock = random.choice([5, 10, 15, 20, 25])

        await self._inventory_service.create_inventory_with_stock(
            owner_type=InventoryOwnerType.PRODUCT,

            owner_id=variant_size.variant_size_id,

            location_id=self._location_id,

            quantity=initial_stock,

            minimum_stock=minimum_stock,

        )

        await self._inventory_movement_service.create_movement(
            movement_type=movement_type,
            owner_type=InventoryOwnerType.PRODUCT,
            owner_id=variant_size.variant_size_id,
            location_id=self._location_id,
            owner_name=variant_size.name,
            owner_code=variant_size.sku,
            quantity=initial_stock,
            prev_stock=0,
            new_stock=initial_stock,
            performed_by=1,
            reference_type=InventoryReferenceType.MANUAL_ADJUSTMENT
        )

async def main() -> None:

    async with UnitOfWork(async_session_factory) as uow:

        pagination_service = PaginationService()


        inventory_service = InventoryService(
            inventory_repository=uow.inventory,
        )


        inventory_movement_service = (
            InventoryMovementService(
                inventory_movement_repo=uow.inventory_movements,
                pagination_service=pagination_service,
            )
        )


        migration = VariantSizeInventoryMigration(
            inventory_repository=uow.inventory,
            inventory_service=inventory_service,
            inventory_movement_service=(
                inventory_movement_service
            ),
            location_id=LOCATION_ID,
        )


        await migration.execute()



if __name__ == "__main__":
    asyncio.run(main())