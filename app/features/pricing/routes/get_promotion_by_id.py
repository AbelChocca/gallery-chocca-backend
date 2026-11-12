from typing import Annotated

from fastapi import (
    Depends,
    Path,
    status,
)

from app.features.pricing.pricing_route import (
    router,
)

from app.features.pricing.schemas.promotion_schema import (
    PromotionDetailResponseSchema,
)

from app.features.pricing.use_cases.get_promotion_detail import (
    GetPromotionDetailUseCase,
)

from app.features.pricing.dependencies.use_cases.get_promotion_detail import (
    get_promotion_detail_use_case,
)

from app.core.authorization.dependencies import (
    require_all_permissions,
)

from app.core.authorization.permissions import (
    Permission,
)


@router.get(
    "/promotions/{promotion_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[
        require_all_permissions(
            Permission.PRICING_READ,
        )
    ],
)
async def get_promotion_detail(
    promotion_id: Annotated[
        int,
        Path(gt=0),
    ],
    use_case: Annotated[
        GetPromotionDetailUseCase,
        Depends(get_promotion_detail_use_case),
    ],
) -> PromotionDetailResponseSchema:

    result = await use_case.execute(
        promotion_id=promotion_id,
    )

    return (
        PromotionDetailResponseSchema
        .model_validate(result)
    )