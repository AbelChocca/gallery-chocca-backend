import asyncio

from app.infra.db.config import async_session_factory
from app.infra.db.uow.unit_of_work import UnitOfWork
from app.features.inventory.services.inventory_service import InventoryService
from app.features.inventory.services.inventory_movement_service import (
    InventoryMovementService,
)
from app.features.material.service import MaterialService
from app.features.inventory.types.inventory_movement import (
    InventoryOwnerType,
)
from app.features.material.entities.material import Material
from app.shared.pagination.pagination_service import PaginationService

LOCATION_ID = 1

class MaterialInventoryMigration:

    def __init__(
        self,
        *,
        material_service: MaterialService,
        inventory_service: InventoryService,
        inventory_movement_service: InventoryMovementService,
        location_id: int,
    ) -> None:
        self._material_service = material_service
        self._inventory_service = inventory_service
        self._inventory_movement_service = inventory_movement_service
        self._location_id = location_id

    async def execute(self) -> None:

        materials = await self._material_service.get_all(
            limit=100000,
        )

        print(f"Found {len(materials.items)} materials.")

        for index, material in enumerate(materials.items, start=1):

            print(
                f"[{index}/{len(materials.items)}] "
                f"Migrating '{material.name}'..."
            )

            await self._create_inventory(material)

        print("Material inventory migration completed successfully.")

    async def _create_inventory(
        self,
        material : Material,
    ) -> None:

        last_movement = (
            await self._inventory_movement_service
            .get_last_material_movement(
                owner_type=InventoryOwnerType.MATERIAL,
                owner_id=material.id
            )
        )

        await self._inventory_service.create_inventory_with_stock(
            owner_type=InventoryOwnerType.MATERIAL,
            owner_id=material.id,
            location_id=self._location_id,
            quantity=material.stock,
            minimum_stock=material.minimum_stock,
            last_movement_at=(
                last_movement.created_at
                if last_movement
                else None
            ),
        )

async def main() -> None:

    async with UnitOfWork(async_session_factory) as uow:

        pagination_service = PaginationService()

        material_service = MaterialService(
            material_repository=uow.materials,
            pagination_service=pagination_service,
        )

        inventory_service = InventoryService(
            inventory_repository=uow.inventory,
        )

        inventory_movement_service = InventoryMovementService(
            inventory_movement_repo=uow.inventory_movements,
            pagination_service=pagination_service,
        )

        migration = MaterialInventoryMigration(
            material_service=material_service,
            inventory_service=inventory_service,
            inventory_movement_service=inventory_movement_service,
            location_id=LOCATION_ID,
        )

        await migration.execute()


if __name__ == "__main__":
    asyncio.run(main())