
from fastapi import Depends, status

from app.features.balancing.routes.other_current_liability.other_current_liability_router import other_current_liability_router
from app.features.balancing.entities.other_current_liability import OtherCurrentLiability
from app.features.balancing.services.other_current_liability_service import OtherCurrentLiabilityService
from app.features.balancing.dependencies.other_current_liability.service import get_other_current_liability_service
from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission
from app.features.balancing.schemas.other_current_liablility_schema import OtherCurrentLiabilityCreateSchema, OtherCurrentLiabilityResponseSchema

@other_current_liability_router.post(
    "",
    response_model=OtherCurrentLiabilityResponseSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[require_permission(Permission.BALANCE_CREATE)]
)
async def create_other_current_liability(
    schema: OtherCurrentLiabilityCreateSchema,
    service: OtherCurrentLiabilityService = Depends(
        get_other_current_liability_service
    ),
) -> OtherCurrentLiabilityResponseSchema:

    entity = OtherCurrentLiability(
        balance_snapshot_id=schema.balance_snapshot_id,
        category=schema.category,
        description=schema.description,
        amount=schema.amount,
        status=schema.status,
    )

    result = await service.create(entity)

    return OtherCurrentLiabilityResponseSchema.model_validate(result)