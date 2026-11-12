from typing import Annotated

from fastapi import (
    Body,
    Depends,
    Path,
    status,
)

from app.features.pricing.pricing_route import router

from app.features.pricing.schemas.promotion_condition_schema import (
    ReplacePromotionConditionsSchema,
)

from app.features.pricing.dtos.promotion_condition import PromotionConditionAssignment
from app.features.pricing.services.promotion_condition import (
    PromotionConditionService,
)
from app.features.pricing.utils.deserialize_dataclass import deserialize_promotion_condition_parameters

from app.features.pricing.dependencies.services.promotion_condition import (
    get_promotion_condition_service,
)

from app.core.authorization.dependencies import (
    require_all_permissions,
)
from app.core.authorization.permissions import (
    Permission,
)



@router.put(
    "/promotions/{promotion_id}/conditions",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        require_all_permissions(
            Permission.PRICING_UPDATE,
            Permission.PRICING_READ,
        )
    ],
)
async def replace_promotion_conditions(
    promotion_id: Annotated[
        int,
        Path(gt=0),
    ],
    schema: Annotated[
        ReplacePromotionConditionsSchema,
        Body(),
    ],
    condition_service: Annotated[
        PromotionConditionService,
        Depends(get_promotion_condition_service),
    ],
) -> None:


    conditions = [
        PromotionConditionAssignment(
            condition_type=condition.condition_type,
            parameters=deserialize_promotion_condition_parameters(
                condition_type=condition.condition_type,
                parameters=condition.parameters.model_dump(),
            ),
            description=condition.description,
        )
        for condition in schema.conditions
    ]

    await condition_service.replace_for_promotion(
        promotion_id=promotion_id,
        conditions=conditions,
    )