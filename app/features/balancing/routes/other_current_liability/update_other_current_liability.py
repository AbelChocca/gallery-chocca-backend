from fastapi import Depends, status

from app.features.balancing.routes.other_current_liability.other_current_liability_router import other_current_liability_router
from app.features.balancing.types.other_current_liability_types import OtherCurrentLiabilityUpdate
from app.features.balancing.services.other_current_liability_service import OtherCurrentLiabilityService
from app.features.balancing.dependencies.other_current_liability.service import get_other_current_liability_service
from app.features.balancing.schemas.other_current_liablility_schema import OtherCurrentLiabilityUpdateSchema

@other_current_liability_router.put(
    "/{other_current_liability_id}",
    status_code=status.HTTP_200_OK,
)
async def update_other_current_liability(
    other_current_liability_id: int,
    payload: OtherCurrentLiabilityUpdateSchema,
    service: OtherCurrentLiabilityService = Depends(get_other_current_liability_service),
):
    update_dto = OtherCurrentLiabilityUpdate(
        category=payload.category,
        description=payload.description,
        amount=payload.amount,
        status=payload.status,
        fields_set=payload.model_fields_set
    )

    return await service.update(
        other_current_liability_id,
        update_dto,
    )