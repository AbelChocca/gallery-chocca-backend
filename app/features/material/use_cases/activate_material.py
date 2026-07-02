from app.features.material.service import MaterialService
from app.infra.cache.redis_service import RedisService
from app.features.material.constants import MATERIAL_CACHE_KEY_TAG

class ActivateMaterialUseCase:

    def __init__(
        self,
        material_service: MaterialService,
        redis_service: RedisService
    ):
        self._material_service = material_service
        self._redis_service = redis_service

    async def execute(self, material_id: int):

        material = await self._material_service.activate(material_id)

        await self._invalidate_cache(material.id)

    async def _invalidate_cache(self, material_id: int):
        await self._redis_service.invalidate_entity(MATERIAL_CACHE_KEY_TAG, material_id)
        await self._redis_service.invalidate_entities(MATERIAL_CACHE_KEY_TAG)