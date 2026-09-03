from fastapi import Depends, status

from app.features.balancing.schemas.inventory_valuation_schema import InventoryValuationUpdateSchema
from app.features.balancing.services.inventory_valuation_service import InventoryValuationService
from app.features.balancing.dependencies.inventory_valuation.service import get_inventory_valuation_service
from app.features.balancing.routes.inventory_valuation.inventory_valuation_router import inventory_valuation_router
from app.features.balancing.types.inventory_valuation_types import InventoryValuationUpdate


@inventory_valuation_router.put(
    "/{inventory_valuation_id}",
    status_code=status.HTTP_200_OK,
)
async def update_inventory_valuation(
    inventory_valuation_id: int,
    payload: InventoryValuationUpdateSchema,
    service: InventoryValuationService = Depends(get_inventory_valuation_service),
):
    update_dto = InventoryValuationUpdate(
        category=payload.category,
        subcategory=payload.subcategory,
        description=payload.description,
        brand=payload.brand,
        location=payload.location,
        quantity=payload.quantity,
        unit_value=payload.unit_value,
        fields_set=payload.model_fields_set
    )

    return await service.update(
        inventory_valuation_id,
        update_dto,
    )