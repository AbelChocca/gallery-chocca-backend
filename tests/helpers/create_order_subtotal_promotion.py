from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.features.pricing.models.model_promotion import PromotionTable
from app.features.pricing.models.model_pricing_rule import PricingRuleTable
from app.features.pricing.models.promotion_pricing_rule import (
    PromotionPricingRuleTable,
)
from app.features.pricing.models.promotion_target import PromotionTargetTable
from app.features.pricing.models.promotion_audience import PromotionAudienceTable
from app.features.pricing.models.promotion_condition import PromotionConditionTable, PromotionConditionType
from app.features.sales.types.customer import CustomerType
from app.features.products.types import BrandType

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


async def create_order_subtotal_promotion(
    db_session: AsyncSession,
    *,
    product_ids: list[int],
    rule_type: PricingRuleType,
    rule_parameters: dict,
    name: str = "Order Subtotal Test Promotion",
    stacking_mode: PromotionStackingMode = PromotionStackingMode.STACKABLE,
    priority: int = 10,
    sale_channel: SaleChannel = SaleChannel.ECOMMERCE,
) -> PromotionTable:

    now = datetime.now(timezone.utc)

    promotion = PromotionTable(
        name=name,
        description="Promotion created for ORDER_SUBTOTAL pricing tests",
        sales_channel=sale_channel,
        stacking_mode=stacking_mode,
        application_scope=PromotionApplicationScope.ORDER_SUBTOTAL,
        priority=priority,
        starts_at=now,
        ends_at=None,
        is_active=True,
    )

    db_session.add(promotion)
    await db_session.flush()

    rule = PricingRuleTable(
        name=f"{name} Rule",
        description="Pricing rule for ORDER_SUBTOTAL test promotion",
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

async def create_wholesale_bgoo_order_promotion(
    db_session: AsyncSession,
) -> PromotionTable:

    now = datetime.now(timezone.utc)

    promotion = PromotionTable(
        name="Mayoristas BGOO - 15%",
        description=(
            "15% de descuento para clientes mayoristas "
            "en compras BGOO desde S/500."
        ),
        sales_channel=SaleChannel.ECOMMERCE,
        stacking_mode=PromotionStackingMode.EXCLUSIVE,
        application_scope=PromotionApplicationScope.ORDER_SUBTOTAL,
        priority=40,
        starts_at=now,
        ends_at=None,
        is_active=True,
    )

    db_session.add(promotion)
    await db_session.flush()

    # ----------------------------
    # Pricing rule
    # ----------------------------

    rule = PricingRuleTable(
        name="15% Mayoristas BGOO",
        description="15% de descuento",
        type=PricingRuleType.PERCENTAGE,
        parameters={
            "percentage": "15",
        },
    )

    db_session.add(rule)
    await db_session.flush()

    db_session.add(
        PromotionPricingRuleTable(
            promotion_id=promotion.id,
            pricing_rule_id=rule.id,
            execution_order=0,
        )
    )

    # ----------------------------
    # Target: BRAND BGOO
    # ----------------------------

    db_session.add(
        PromotionTargetTable(
            promotion_id=promotion.id,
            target_type=PromotionTargetType.BRAND,
            reference_id=None,
            reference_value=BrandType.BGOO.value,
        )
    )

    # ----------------------------
    # Audience: WHOLESALE
    # ----------------------------

    db_session.add(
        PromotionAudienceTable(
            promotion_id=promotion.id,
            audience_type=PromotionAudienceType.CUSTOMER_TYPE,
            reference_id=None,
            reference_value=CustomerType.WHOLESALE.value,
        )
    )

    # ----------------------------
    # Condition: minimum S/500
    # ----------------------------

    db_session.add(
        PromotionConditionTable(
            promotion_id=promotion.id,
            condition_type=PromotionConditionType.MINIMUM_ORDER_AMOUNT,
            parameters={
                "minimum_amount": "500.00",
            },
            description="Compra mínima de S/500",
        )
    )

    await db_session.commit()
    await db_session.refresh(promotion)

    return promotion