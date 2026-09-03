from fastapi import Depends

from app.features.balancing.schemas.inventory_valuation_schema import InventoryValuationResponseSchema, InventoryValuationFilterSchema
from app.features.balancing.services.inventory_valuation_service import InventoryValuationService
from app.features.balancing.dependencies.inventory_valuation.service import get_inventory_valuation_service
from app.features.balancing.routes.inventory_valuation.inventory_valuation_router import inventory_valuation_router

@inventory_valuation_router.get(
    "",
    response_model=list[
        InventoryValuationResponseSchema
    ],
)
async def get_inventory_valuations(
    filters: InventoryValuationFilterSchema = Depends(),
    service: InventoryValuationService = Depends(
        get_inventory_valuation_service
    ),
):
    result = await service.find(
        balance_snapshot_id=filters.balance_snapshot_id,
        category=filters.category,
        subcategory=filters.subcategory,
        brand=filters.brand,
        location=filters.location,
    )

    return result