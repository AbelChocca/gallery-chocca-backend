from typing import Annotated

from pydantic import TypeAdapter
from fastapi import Body, Depends, status

from app.features.pricing.pricing_route import (
    router,
)

from app.features.pricing.schemas.promotion_schema import (
    CreatePromotionSchema,
    PromotionResponseSchema
)

from app.features.pricing.dtos.promotion_dto import (
    CreatePromotionDTO,
)

from app.features.pricing.use_cases.create_promotion import (
    CreatePromotionUseCase,
)

from app.features.pricing.dependencies.use_cases.create_promotion import (
    get_create_promotion_use_case,
)

from app.core.authorization.dependencies import (
    require_all_permissions,
)

from app.core.authorization.permissions import (
    Permission,
)

create_promotion_adapter = TypeAdapter(
    CreatePromotionDTO
)


@router.post(
    "/promotions",
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        require_all_permissions(
            Permission.PRICING_CREATE,
            Permission.PRICING_READ,
            Permission.PRICING_UPDATE,
        )
    ],
)
async def create_promotion(
    schema: Annotated[
        CreatePromotionSchema,
        Body(),
    ],
    use_case: Annotated[
        CreatePromotionUseCase,
        Depends(get_create_promotion_use_case),
    ],
) -> PromotionResponseSchema:
    command = create_promotion_adapter.validate_python(
        schema.model_dump()
    )

    result = await use_case.execute(
        command=command,
    )

    return PromotionResponseSchema.model_validate(result)