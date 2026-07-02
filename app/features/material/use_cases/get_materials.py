from app.features.material.service import MaterialService
from app.features.media.service import MediaService
from app.infra.cache.redis_service import RedisService
from app.features.media.types import ImageType
from app.features.material.dto import MaterialFilters, MaterialCatalogDTO, MaterialCatalogPaginatedDTO
from app.features.material.constants import MATERIAL_CACHE_KEY_TAG

class GetMaterialsUseCase:
    def __init__(
        self,
        material_service: MaterialService,
        media_service: MediaService,
        cache_service: RedisService
    ):
        self._material_service = material_service
        self._media_service = media_service
        self._cache_service = cache_service

    async def _build_catalog(
        self,
        *,
        filters: MaterialFilters | None,
        page: int,
        limit: int
    ) -> MaterialCatalogPaginatedDTO:

        result = await self._material_service.get_all(
            filters=filters,
            page=page,
            limit=limit
        )

        materials = result.items

        material_ids = [
            material.id
            for material in materials
        ]

        images = await self._media_service.get_images_by_owner_ids(
            owner_type=ImageType.material,
            owner_ids=material_ids
        )

        image_map = {
            image.owner_id: image
            for image in images
        }

        catalog_items = [
            MaterialCatalogDTO.from_entities(
                material=material,
                image=image_map.get(material.id)
            )
            for material in materials
        ]

        return MaterialCatalogPaginatedDTO.create(
            items=catalog_items,
            total_items=result.total_items,
            current_page=result.pagination.current_page,
            total_pages=result.pagination.total_pages
        )

    async def execute(
        self,
        *,
        filters: MaterialFilters | None = None,
        page: int = 1,
        limit: int = 20
    ) -> MaterialCatalogPaginatedDTO:
        return await self._cache_service.get_or_set_with_lock_v2(
            tag=MATERIAL_CACHE_KEY_TAG,
            callback=self._build_catalog,
            kwargs={
                "filters": filters,
                "page": page,
                "limit": limit
            },
            key_args={
                "filters": (
                    filters.to_dict
                    if filters
                    else {}
                ),
                "page": page,
                "limit": limit
            },
            serializer=lambda dto: dto.to_dict(),
            deserializer=MaterialCatalogPaginatedDTO.from_dict
        )