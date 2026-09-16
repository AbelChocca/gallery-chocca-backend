from datetime import datetime

from app.features.pricing.models.model_pricing_rule import PricingRuleTable
from app.features.pricing.models.model_promotion import PromotionTable
from app.features.pricing.models.promotion_audience import (
    PromotionAudienceTable,
)
from app.features.pricing.models.promotion_pricing_rule import (
    PromotionPricingRuleTable,
)
from app.features.pricing.models.promotion_target import (
    PromotionTargetTable,
)
from app.features.pricing.types.pricing_rules_types import PricingRuleType
from app.features.pricing.types.promotion_types import (
    PromotionAudienceType,
    PromotionStackingMode,
    PromotionTargetType,
)
from app.features.sales.types.sale import SaleChannel
from app.features.products.types import CategoryType

async def create_test_promotion(
    db_session,
    *,
    product_id: int,
    is_active: bool = True,
    starts_at: datetime | None = None,
    ends_at: datetime | None = None,
) -> PromotionTable:
    promotion = PromotionTable(
        name="Promotion Condition Test",
        description="Promoción para pruebas de condiciones",
        sales_channel=SaleChannel.ECOMMERCE,
        stacking_mode=PromotionStackingMode.STACKABLE,
        priority=10,
        starts_at=starts_at,
        ends_at=ends_at,
        is_active=is_active,
    )

    db_session.add(promotion)
    await db_session.commit()
    await db_session.refresh(promotion)

    rule = PricingRuleTable(
        name="Promotion Condition Test - 10 Percent",
        description="Descuento porcentual del 10%",
        type=PricingRuleType.PERCENTAGE,
        parameters={"value": "10"},
    )

    db_session.add(rule)
    await db_session.commit()
    await db_session.refresh(rule)

    promotion_rule = PromotionPricingRuleTable(
        promotion_id=promotion.id,
        pricing_rule_id=rule.id,
        execution_order=0,
    )

    target = PromotionTargetTable(
        promotion_id=promotion.id,
        target_type=PromotionTargetType.PRODUCT,
        reference_id=product_id,
    )

    audience = PromotionAudienceTable(
        promotion_id=promotion.id,
        audience_type=PromotionAudienceType.ALL_CUSTOMERS,
    )

    db_session.add_all([
        promotion_rule,
        target,
        audience,
    ])
    await db_session.commit()

    return promotion

async def create_category_target_promotion(
    db_session,
    *,
    category: CategoryType,
    discount: str = "10",
) -> PromotionTable:
    promotion = PromotionTable(
        name=f"Promotion Category {category.value}",
        description=f"Promoción dirigida a categoría {category.value}",
        sales_channel=SaleChannel.ECOMMERCE,
        stacking_mode=PromotionStackingMode.STACKABLE,
        priority=10,
        starts_at=None,
        ends_at=None,
        is_active=True,
    )

    db_session.add(promotion)
    await db_session.commit()
    await db_session.refresh(promotion)

    rule = PricingRuleTable(
        name=f"{discount}% OFF {category.value}",
        description="Descuento porcentual para test de target por categoría",
        type=PricingRuleType.PERCENTAGE,
        parameters={"value": discount},
    )

    db_session.add(rule)
    await db_session.commit()
    await db_session.refresh(rule)

    promotion_rule = PromotionPricingRuleTable(
        promotion_id=promotion.id,
        pricing_rule_id=rule.id,
        execution_order=0,
    )

    target = PromotionTargetTable(
        promotion_id=promotion.id,
        target_type=PromotionTargetType.CATEGORY,
        reference_id=None,
        reference_value=category.value,
    )

    audience = PromotionAudienceTable(
        promotion_id=promotion.id,
        audience_type=PromotionAudienceType.ALL_CUSTOMERS,
    )

    db_session.add_all([
        promotion_rule,
        target,
        audience,
    ])

    await db_session.commit()

    return promotion