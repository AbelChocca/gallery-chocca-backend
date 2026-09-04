from app.infra.db.uow.dependency import get_uow
from app.infra.db.uow.unit_of_work import UnitOfWork
from app.features.balancing.services.inventory_valuation_service import InventoryValuationService


from fastapi import Depends

def get_inventory_valuation_service(
    uow: UnitOfWork = Depends(get_uow)
) -> InventoryValuationService:

    return InventoryValuationService(
        inventory_valuation_repository=uow.inventory_valuations
    )