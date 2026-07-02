from fastapi import Depends

from app.features.material.service import MaterialService
from app.features.media.service import MediaService
from app.features.media.dependency import get_media_service
from app.infra.saga.saga_service import SagaService, get_saga_service
from app.infra.cache.dependency import get_cache_service
from app.infra.cache.redis_service import RedisService

from app.infra.db.uow.unit_of_work import UnitOfWork
from app.infra.db.uow.dependency import get_uow

from app.shared.pagination.pagination_service import PaginationService, get_pagination_service

from app.features.material.use_cases.create_material import CreateMaterialUseCase
from app.features.material.use_cases.get_materials import GetMaterialsUseCase
from app.features.material.use_cases.deactivate_material import DeactivateMaterialUseCase
from app.features.material.use_cases.activate_material import ActivateMaterialUseCase
from app.features.material.use_cases.get_material_by_id import GetMaterialByIdUseCase


def get_material_service(
    uow: UnitOfWork = Depends(get_uow),
    pagination_service: PaginationService = Depends(
        get_pagination_service
    )
) -> MaterialService:
    return MaterialService(
        material_repository=uow.materials,
        pagination_service=pagination_service
    )

def get_create_material_case(
        material_service: MaterialService = Depends(get_material_service),
        media_service: MediaService = Depends(get_media_service),
        saga_service: SagaService = Depends(get_saga_service),
        cache_service: RedisService = Depends(get_cache_service)
) -> CreateMaterialUseCase:
    return CreateMaterialUseCase(
        material_service=material_service,
        media_service=media_service,
        saga_service=saga_service,
        cache_service=cache_service
    )

def get_materials_case(
    material_service: MaterialService = Depends(
        get_material_service
    ),
    media_service: MediaService = Depends(
        get_media_service
    ),
    cache_service: RedisService = Depends(
        get_cache_service
    )
) -> GetMaterialsUseCase:
    return GetMaterialsUseCase(
        material_service=material_service,
        media_service=media_service,
        cache_service=cache_service
    )

def get_activate_material_case(
    material_service: MaterialService = Depends(get_material_service),
    cache_service: RedisService = Depends(get_cache_service)
) -> ActivateMaterialUseCase:

    return ActivateMaterialUseCase(
        material_service=material_service,
        redis_service=cache_service
    )

def get_deactivate_material_case(
    material_service: MaterialService = Depends(get_material_service),
    cache_service: RedisService = Depends(get_cache_service)
) -> DeactivateMaterialUseCase:

    return DeactivateMaterialUseCase(
        material_service=material_service,
        redis_service=cache_service
    )

def get_material_by_id_case(
    material_service: MaterialService = Depends(
        get_material_service
    ),
    media_service: MediaService = Depends(
        get_media_service
    ),
    cache_service: RedisService = Depends(
        get_cache_service
    )
) -> GetMaterialByIdUseCase:
    return GetMaterialByIdUseCase(
        material_service=material_service,
        media_service=media_service,
        cache_service=cache_service
    )