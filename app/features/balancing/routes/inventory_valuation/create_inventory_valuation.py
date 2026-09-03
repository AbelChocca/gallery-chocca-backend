from fastapi import Depends, status

from app.features.balancing.schemas.inventory_valuation_schema import InventoryValuationCreateSchema, InventoryValuationResponseSchema
from app.features.balancing.services.inventory_valuation_service import InventoryValuationService
from app.features.balancing.dependencies.inventory_valuation.service import get_inventory_valuation_service
from app.features.balancing.routes.inventory_valuation.inventory_valuation_router import inventory_valuation_router
from app.features.balancing.entities.inventory_valuation import InventoryValuation

@inventory_valuation_router.post(
    "",
    response_model=InventoryValuationResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_inventory_valuation(
    schema: InventoryValuationCreateSchema,
    service: InventoryValuationService = Depends(
        get_inventory_valuation_service
    ),
) -> InventoryValuationResponseSchema:

    entity = InventoryValuation(
        balance_snapshot_id=schema.balance_snapshot_id,
        category=schema.category,
        subcategory=schema.subcategory,
        description=schema.description,
        brand=schema.brand,
        location=schema.location,
        quantity=schema.quantity,
        unit_value=schema.unit_value,
    )

    result = await service.create(entity)

    return InventoryValuationResponseSchema.model_validate(result)