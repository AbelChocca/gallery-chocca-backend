from app.features.material.service import MaterialService
from app.features.media.service import MediaService
from app.features.material.dto import CreateMaterialDTO
from app.infra.saga.saga_service import SagaService
from app.features.material.constants import MATERIAL_FOLDER
from app.features.media.types import ImageType
from app.infra.saga.saga_use_case import UseCaseSaga
from app.features.material.entity import Material
from app.infra.cache.redis_service import RedisService
from app.features.material.constants import MATERIAL_CACHE_KEY_TAG

from typing import BinaryIO

class CreateMaterialUseCase(UseCaseSaga):
    def __init__(
        self,
        material_service: MaterialService,
        media_service: MediaService,
        saga_service: SagaService,
        cache_service: RedisService,
    ):
        super().__init__(saga_service)

        self._material_service = material_service
        self._media_service = media_service
        self._cache_service = cache_service

    async def execute(
        self,
        command: CreateMaterialDTO,
        image_file: BinaryIO | None = None
    ) -> Material:  
        async def operation() -> Material:
            material = await self._material_service.create(
                command
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

        await self._cache_service.invalidate_entities(
            tag=MATERIAL_CACHE_KEY_TAG
        )

        return material