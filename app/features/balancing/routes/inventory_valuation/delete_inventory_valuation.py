from fastapi import Depends, status

from app.features.balancing.services.inventory_valuation_service import InventoryValuationService
from app.features.balancing.dependencies.inventory_valuation.service import get_inventory_valuation_service
from app.features.balancing.routes.inventory_valuation.inventory_valuation_router import inventory_valuation_router


@inventory_valuation_router.delete(
    "/{inventory_valuation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_inventory_valuation(
    inventory_valuation_id: int,
    service: InventoryValuationService = Depends(
        get_inventory_valuation_service
    ),
) -> None:
    await service.delete(inventory_valuation_id)