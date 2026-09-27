from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.features.pricing.models.model_promotion import PromotionTable
from app.features.pricing.models.model_pricing_rule import PricingRuleTable
from app.features.pricing.models.promotion_pricing_rule import (
    PromotionPricingRuleTable,
)
from app.features.pricing.models.promotion_target import PromotionTargetTable
from app.features.pricing.models.promotion_audience import (
    PromotionAudienceTable,
)

from app.features.pricing.types.promotion_types import (
    PromotionApplicationScope,
    PromotionStackingMode,
    PromotionTargetType,
    PromotionAudienceType,
)
from app.features.pricing.types.pricing_rules_types import (
    PricingRuleType,
)
from app.features.sales.types.sale import SaleChannel


async def create_per_item_promotion(
    db_session: AsyncSession,
    *,
    product_ids: list[int],
    rule_type: PricingRuleType,
    rule_parameters: dict,
    name: str = "Per Item Test Promotion",
    stacking_mode: PromotionStackingMode = PromotionStackingMode.STACKABLE,
    priority: int = 10,
    sale_channel: SaleChannel = SaleChannel.ECOMMERCE,
) -> PromotionTable:

    now = datetime.now(timezone.utc)

    promotion = PromotionTable(
        name=name,
        description="Promotion created for PER_ITEM pricing tests",
        sales_channel=sale_channel,
        stacking_mode=stacking_mode,
        application_scope=PromotionApplicationScope.PER_ITEM,
        priority=priority,
        starts_at=now,
        ends_at=None,
        is_active=True,
    )

    db_session.add(promotion)
    await db_session.flush()

    rule = PricingRuleTable(
        name=f"{name} Rule",
        description="Pricing rule for PER_ITEM test promotion",
        type=rule_type,
        parameters=rule_parameters,
    )

    db_session.add(rule)
    await db_session.flush()

    link = PromotionPricingRuleTable(
        promotion_id=promotion.id,
        pricing_rule_id=rule.id,
        execution_order=0,
    )

    db_session.add(link)

    targets = [
        PromotionTargetTable(
            promotion_id=promotion.id,
            target_type=PromotionTargetType.PRODUCT,
            reference_id=product_id,
        )
        for product_id in product_ids
    ]

    db_session.add_all(targets)

    audience = PromotionAudienceTable(
        promotion_id=promotion.id,
        audience_type=PromotionAudienceType.ALL_CUSTOMERS,
    )

    db_session.add(audience)

    await db_session.commit()
    await db_session.refresh(promotion)

    return promotion