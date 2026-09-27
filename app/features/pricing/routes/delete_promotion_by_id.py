from typing import Annotated

from fastapi import (
    Depends,
    Path,
    status,
)

from app.features.pricing.pricing_route import (
    router,
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


@router.delete(
    "/promotions/{promotion_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        require_all_permissions(
            Permission.PRICING_UPDATE,
        )
    ],
)
async def delete_promotion(
    promotion_id: Annotated[
        int,
        Path(gt=0),
    ],
    service: Annotated[
        PromotionService,
        Depends(get_promotion_service),
    ],
) -> None:

    await service.delete(
        promotion_id=promotion_id,
    )