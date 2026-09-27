from typing import Annotated

from fastapi import (
    Body,
    Depends,
    Path,
    status,
)

from app.features.pricing.pricing_route import (
    router,
)

from app.features.pricing.schemas.promotion_schema import (
    UpdatePromotionSchema,
)

from app.features.pricing.services.promotion import (
    PromotionService,
)

from app.features.pricing.dependencies.services.promotion import (
    get_promotion_service,
)

from app.core.authorization.dependencies import (
    require_all_permissions,
)

from app.core.authorization.permissions import (
    Permission,
)


@router.patch(
    "/promotions/{promotion_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        require_all_permissions(
            Permission.PRICING_UPDATE,
            Permission.PRICING_READ,
        )
    ],
)
async def update_promotion(
    promotion_id: Annotated[
        int,
        Path(gt=0),
    ],
    schema: Annotated[
        UpdatePromotionSchema,
        Body(),
    ],
    service: Annotated[
        PromotionService,
        Depends(get_promotion_service),
    ],
) -> None:

    changes = schema.model_dump(
        exclude_unset=True,
    )

    await service.update(
        promotion_id=promotion_id,
        changes=changes,
    )