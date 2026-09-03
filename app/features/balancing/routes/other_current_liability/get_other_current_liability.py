from fastapi import Depends

from app.features.balancing.routes.other_current_liability.other_current_liability_router import other_current_liability_router
from app.features.balancing.services.other_current_liability_service import OtherCurrentLiabilityService
from app.features.balancing.dependencies.other_current_liability.service import get_other_current_liability_service
from app.features.balancing.schemas.other_current_liablility_schema import OtherCurrentLiabilityResponseSchema

@other_current_liability_router.get(
    "/{other_current_liability_id}",
    response_model=OtherCurrentLiabilityResponseSchema,
)
async def get_other_current_liability(
    other_current_liability_id: int,
    service: OtherCurrentLiabilityService = Depends(
        get_other_current_liability_service
    ),
):
    result = await service.get_by_id(other_current_liability_id)

    return OtherCurrentLiabilityResponseSchema.model_validate(result)