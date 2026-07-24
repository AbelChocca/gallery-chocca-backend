from app.features.material.service import MaterialService
from app.features.media.service import MediaService
from app.features.material.dto.material import CreateMaterialDTO
from app.infra.saga.saga_service import SagaService
from app.features.material.constants import MATERIAL_FOLDER
from app.features.media.types import ImageType
from app.infra.saga.saga_use_case import UseCaseSaga
from app.features.material.entities.material import Material
from app.features.inventory.services.inventory_service import InventoryService
from app.features.inventory.services.inventory_movement_service import InventoryMovementService
from app.features.inventory.types.inventory_movement import InventoryOwnerType, InventoryMovementType

from typing import BinaryIO
from decimal import Decimal

class CreateMaterialUseCase(UseCaseSaga):
    def __init__(
        self,
        material_service: MaterialService,
        media_service: MediaService,
        saga_service: SagaService,
        inventory_service: InventoryService,
        inventory_movement_service: InventoryMovementService,
    ):
        super().__init__(saga_service)

        self._material_service = material_service
        self._media_service = media_service
        self._inventory_service = inventory_service
        self._inventory_movement_service = inventory_movement_service

    async def execute(
        self,
        command: CreateMaterialDTO,
        user_id: int,
        image_file: BinaryIO | None = None
    ) -> Material:  
        async def operation() -> Material:
            material = await self._material_service.create(
                command
            )

            await self._create_initial_inventory(
                material=material,
                user_id=user_id,
                command=command,
            )

            if image_file:
                file = await self._saga.execute_step(
                    action=self._media_service.upload_image,
                    action_kwargs={
                        "image_resource": image_file,
                        "folder": MATERIAL_FOLDER,
                    },
                    compensation_factory=lambda image: (
                        self._media_service.move_image_to_trash,
                        self._media_service.move_image_to_trash.__name__,
                        {
                            "public_id": image.public_id
                        }
                    )
                )

                await self._media_service.create_image_v2(
                    image_url=file.url,
                    public_id=file.public_id,
                    owner_id=material.id,
                    owner_type=ImageType.material
                )

            return material

        material = await self._saga.execute_safely(operation)

        return material

    async def _create_initial_inventory(
        self,
        *,
        material: Material,
        user_id: int,
        command: CreateMaterialDTO,
    ) -> None:

        for inventory in command.inventories:

            await self._inventory_service.create_inventory_with_stock(
                owner_type=InventoryOwnerType.MATERIAL,
                owner_id=material.id,
                location_id=inventory.location_id,
                quantity=inventory.initial_stock,
                minimum_stock=inventory.minimum_stock,
            )

            if inventory.initial_stock is None:
                continue

            await self._inventory_movement_service.create_movement(
                movement_type=InventoryMovementType.ENTRY,
                owner_type=InventoryOwnerType.MATERIAL,
                owner_id=material.id,
                location_id=inventory.location_id,

                owner_name=material.name,
                owner_code=material.code,

                quantity=inventory.initial_stock,

                prev_stock=Decimal("0"),
                new_stock=inventory.initial_stock,

                performed_by=user_id,

                reason="Entrada de stock de material.",
            )