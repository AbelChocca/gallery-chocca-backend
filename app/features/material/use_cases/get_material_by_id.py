from app.features.material.service import MaterialService
from app.features.media.service import MediaService
from app.infra.cache.redis_service import RedisService

from app.features.material.dto import MaterialResponseDTO
from app.features.media.types import ImageType
from app.features.material.constants import MATERIAL_CACHE_KEY_TAG


class GetMaterialByIdUseCase:
    def __init__(
        self,
        material_service: MaterialService,
        media_service: MediaService,
        cache_service: RedisService
    ):
        self._material_service = material_service
        self._media_service = media_service
        self._cache_service = cache_service

    async def _build_material_detail(
        self,
        *,
        material_id: int
    ) -> MaterialResponseDTO:
        material = await self._material_service.get_by_id(material_id)

        images = await self._media_service.get_images_by_owner_ids(
            owner_type=ImageType.material,
            owner_ids=[material.id]
        )

        image = images[0] if images else None

        return MaterialResponseDTO.from_entities(
            material=material,
            image=image
        )

    async def execute(
        self,
        material_id: int
    ) -> MaterialResponseDTO:
        return await self._cache_service.get_or_set_with_lock_v2(
            tag=MATERIAL_CACHE_KEY_TAG,
            callback=self._build_material_detail,
            kwargs={
                "material_id": material_id
            },
            key_args={
                "material_id": material_id
            },
            serializer=lambda dto: dto.to_dict(),
            deserializer=MaterialResponseDTO.from_dict
        )