from app.features.material.service import MaterialService
from app.features.media.service import MediaService
from app.features.material.dto.material import UpdateMaterialDTO
from app.infra.saga.saga_service import SagaService
from app.features.material.constants import MATERIAL_FOLDER
from app.features.media.types import ImageType
from app.infra.saga.saga_use_case import UseCaseSaga
from app.features.material.entities.material import Material
from app.infra.cache.redis_service import RedisService
from app.features.material.constants import MATERIAL_CACHE_KEY_TAG
from app.core.exceptions import ValidationError

from typing import BinaryIO

class UpdateMaterialUseCase(UseCaseSaga):
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
        material_id: int,
        command: UpdateMaterialDTO,
        image_file: BinaryIO | None = None
    ) -> Material:
        if command.delete_image and image_file is not None:
            raise ValidationError(
                "No se puede eliminar y reemplazar una imagen al mismo tiempo.",
                {
                    "module": "materials",
                    "case": "update_material",
                }
            )

        async def operation():

            material = await self._material_service.update(
                material_id=material_id,
                dto=command
            )

            current_image = await self._media_service.get_first_image_by_owner(
                owner_type=ImageType.material,
                owner_id=material.id
            )


            if command.delete_image:
                if current_image:
                    await self._saga.execute_step(
                        action=self._media_service.move_image_to_trash,
                        action_kwargs={
                            "public_id": current_image.public_id
                        },
                        compensation_factory=lambda _: (
                            self._media_service.recover_image_from_trash,
                            self._media_service.recover_image_from_trash.__name__,
                            {
                                "public_id": current_image.public_id
                            }
                        )
                    )

                    await self._media_service.delete_image_v2(
                        image_public_id=current_image.public_id
                    )

                return material

            if image_file is None:
                return material

            if current_image:
                await self._saga.execute_step(
                    action=self._media_service.move_image_to_trash,
                    action_kwargs={
                        "public_id": current_image.public_id
                    },
                    compensation_factory=lambda _: (
                        self._media_service.recover_image_from_trash,
                        self._media_service.recover_image_from_trash.__name__,
                        {
                            "public_id": current_image.public_id
                        }
                    )
                )

            uploaded = await self._saga.execute_step(
                action=self._media_service.upload_image,
                action_kwargs={
                    "image_resource": image_file,
                    "folder": MATERIAL_FOLDER
                },
                compensation_factory=lambda image: (
                    self._media_service.move_image_to_trash,
                    self._media_service.move_image_to_trash.__name__,
                    {
                        "public_id": image.public_id
                    }
                )
            )

            if current_image:
                await self._media_service.update_image(
                    image=current_image,
                    public_id=uploaded.public_id,
                    image_url=uploaded.url
                )
            else:
                await self._media_service.create_image_v2(
                    image_url=uploaded.url,
                    public_id=uploaded.public_id,
                    owner_id=material.id,
                    owner_type=ImageType.material
                )

            return material

        material = await self._saga.execute_safely(operation)

        await self._cache_service.invalidate_entities(
            MATERIAL_CACHE_KEY_TAG
        )

        await self._cache_service.invalidate_entity(
            MATERIAL_CACHE_KEY_TAG,
            material.id
        )

        return material