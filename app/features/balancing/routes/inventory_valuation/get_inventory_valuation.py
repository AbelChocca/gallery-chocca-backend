from fastapi import Depends

from app.features.balancing.schemas.inventory_valuation_schema import InventoryValuationResponseSchema
from app.features.balancing.services.inventory_valuation_service import InventoryValuationService
from app.features.balancing.dependencies.inventory_valuation.service import get_inventory_valuation_service
from app.features.balancing.routes.inventory_valuation.inventory_valuation_router import inventory_valuation_router

@inventory_valuation_router.get(
    "/{inventory_valuation_id}",
    response_model=InventoryValuationResponseSchema,
)
async def get_inventory_valuation(
    inventory_valuation_id: int,
    service: InventoryValuationService = Depends(
        get_inventory_valuation_service
    ),
):
    result = await service.get_by_id(inventory_valuation_id)

    return InventoryValuationResponseSchema.model_validate(result)