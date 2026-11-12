from typing import Annotated

from fastapi import (
    Body,
    Depends,
    Path,
    status,
)

from app.features.pricing.pricing_route import router

from app.features.pricing.schemas.promotion_target_schema import (
    ReplacePromotionTargetsSchema,
)
from app.features.pricing.services.promotion_target import (
    PromotionTargetService,
)
from app.features.pricing.dependencies.services.promotion_target import (
    get_promotion_target_service,
)

from app.features.pricing.dtos.promotion_target import (
    PromotionTargetAssignment,
)

from app.core.authorization.dependencies import (
    require_all_permissions,
)
from app.core.authorization.permissions import (
    Permission,
)


@router.put(
    "/promotions/{promotion_id}/targets",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        require_all_permissions(
            Permission.PRICING_UPDATE,
            Permission.PRICING_READ,
        )
    ],
)
async def replace_promotion_targets(
    promotion_id: Annotated[
        int,
        Path(gt=0),
    ],
    schema: Annotated[
        ReplacePromotionTargetsSchema,
        Body(),
    ],
    target_service: Annotated[
        PromotionTargetService,
        Depends(get_promotion_target_service),
    ],
) -> None:

    targets = [
        PromotionTargetAssignment(
            target_type=target.target_type,
            reference_id=target.reference_id,
            reference_value=target.reference_value,
        )
        for target in schema.targets
    ]

    await target_service.replace_for_promotion(
        promotion_id=promotion_id,
        targets=targets,
    )