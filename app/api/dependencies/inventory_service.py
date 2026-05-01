from app.application.inventory_service import InventoryService
from app.api.dependencies.uow import get_uow
from app.infra.db.unit_of_work import UnitOfWork
from app.api.dependencies.cache.services import get_cache_service
from app.infra.cache.protocole import CacheProtocol
from app.shared.services.pagination.pagination_service import PaginationService, get_pagination_service

from fastapi import Depends

def get_inventory_service(
        uow: UnitOfWork = Depends(get_uow),
        cache_service: CacheProtocol = Depends(get_cache_service),
        pagination_service: PaginationService = Depends(get_pagination_service)
        ) -> InventoryService:
    return InventoryService(
        product_repository=uow.products,
        inventory_movement_repo=uow.inventory,
        image_repository=uow.images,
        cache_service=cache_service,
        pagination_service=pagination_service
    )