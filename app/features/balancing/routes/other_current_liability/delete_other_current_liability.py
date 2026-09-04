from fastapi import Depends, status

from app.features.balancing.routes.other_current_liability.other_current_liability_router import other_current_liability_router
from app.features.balancing.services.other_current_liability_service import OtherCurrentLiabilityService
from app.features.balancing.dependencies.other_current_liability.service import get_other_current_liability_service

@other_current_liability_router.delete(
    "/{other_current_liability_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_other_current_liability(
    other_current_liability_id: int,
    service: OtherCurrentLiabilityService = Depends(
        get_other_current_liability_service
    ),
) -> None:
    await service.delete(other_current_liability_id)