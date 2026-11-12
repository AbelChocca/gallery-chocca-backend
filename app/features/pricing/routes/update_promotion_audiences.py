from typing import Annotated

from fastapi import (
    Body,
    Depends,
    Path,
    status,
)

from app.features.pricing.pricing_route import router

from app.features.pricing.schemas.promotion_audience_schema import (
    ReplacePromotionAudiencesSchema,
)

from app.features.pricing.dtos.promotion_audience_dto import PromotionAudienceAssignment
from app.features.pricing.services.promotion_audience import (
    PromotionAudienceService,
)

from app.features.pricing.dependencies.services.promotion_audience import (
    get_promotion_audience_service,
)

from app.core.authorization.dependencies import (
    require_all_permissions,
)
from app.core.authorization.permissions import (
    Permission,
)


@router.put(
    "/promotions/{promotion_id}/audiences",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        require_all_permissions(
            Permission.PRICING_UPDATE,
            Permission.PRICING_READ,
        )
    ],
)
async def replace_promotion_audiences(
    promotion_id: Annotated[
        int,
        Path(gt=0),
    ],
    schema: Annotated[
        ReplacePromotionAudiencesSchema,
        Body(),
    ],
    audience_service: Annotated[
        PromotionAudienceService,
        Depends(get_promotion_audience_service),
    ],
) -> None:

    audiences = [
            PromotionAudienceAssignment(
                **audience.model_dump()
            )
            for audience in schema.audiences
        ]
        

    await audience_service.replace_for_promotion(
        promotion_id=promotion_id,
        audiences=audiences,
    )