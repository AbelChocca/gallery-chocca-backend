from typing import Annotated

from fastapi import (
    Body,
    Depends,
    Path,
    status,
)

from app.features.pricing.pricing_route import router

from app.features.pricing.schemas.pricing_rule_schema import (
    ReplacePromotionPricingRulesSchema,
)

from app.features.pricing.dtos.promotion_pricing_rule_dto import PromotionPricingRuleAssignment
from app.features.pricing.services.promotion_pricing_rule import (
    PromotionPricingRuleService,
)
from app.features.pricing.dependencies.services.promotion_pricing_rule import (
    get_promotion_pricing_rule_service,
)

from app.core.authorization.dependencies import (
    require_all_permissions,
)
from app.core.authorization.permissions import (
    Permission,
)


@router.put(
    "/promotions/{promotion_id}/pricing-rules",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        require_all_permissions(
            Permission.PRICING_UPDATE,
            Permission.PRICING_READ,
        )
    ],
)
async def replace_promotion_pricing_rules(
    promotion_id: Annotated[
        int,
        Path(gt=0),
    ],
    schema: Annotated[
        ReplacePromotionPricingRulesSchema,
        Body(),
    ],
    pricing_rule_service: Annotated[
        PromotionPricingRuleService,
        Depends(
            get_promotion_pricing_rule_service
        ),
    ],
) -> None:

    rules = [
        PromotionPricingRuleAssignment(
            pricing_rule_id=rule.pricing_rule_id,
            execution_order=rule.execution_order,
        )
        for rule in schema.pricing_rules
    ]

    await pricing_rule_service.replace_for_promotion(
        promotion_id=promotion_id,
        rules=rules,
    )