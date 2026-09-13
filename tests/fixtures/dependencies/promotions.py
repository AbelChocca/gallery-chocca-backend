from datetime import datetime, timezone
from decimal import Decimal
from sqlmodel.ext.asyncio.session import AsyncSession

import pytest_asyncio

from app.features.pricing.models.model_pricing_rule import PricingRuleTable
from app.features.pricing.models.model_promotion import PromotionTable
from app.features.pricing.models.promotion_audience import (
    PromotionAudienceTable,
)
from app.features.pricing.models.promotion_condition import (
    PromotionConditionTable,
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
    PromotionConditionType,
    PromotionStackingMode,
    PromotionTargetType,
)
from app.features.sales.types.sale import SaleChannel


@pytest_asyncio.fixture
async def pricing_promotions(db_session:AsyncSession, pricing_products):
    products = pricing_products["products"]

    now = datetime.now(timezone.utc)

    promotion_1 = PromotionTable(
        name="Pricing Test - 10% OFF",
        description="Promocion porcentual para pruebas de pricing",
        sales_channel=SaleChannel.ECOMMERCE,
        stacking_mode=PromotionStackingMode.STACKABLE,
        priority=10,
        starts_at=now,
        ends_at=None,
        is_active=True,
    )

    promotion_2 = PromotionTable(
        name="Pricing Test - S/20 OFF",
        description="Promocion exclusiva para clientes mayoristas",
        sales_channel=SaleChannel.ECOMMERCE,
        stacking_mode=PromotionStackingMode.EXCLUSIVE,
        priority=20,
        starts_at=now,
        ends_at=None,
        is_active=True,
    )

    db_session.add_all([
        promotion_1,
        promotion_2,
    ])
    await db_session.commit()

    await db_session.refresh(promotion_1)
    await db_session.refresh(promotion_2)

    # ---------------------------------------------------------
    # Pricing rules
    # ---------------------------------------------------------

    percentage_rule = PricingRuleTable(
        name="Pricing Test - 10 Percent",
        description="Descuento porcentual del 10%",
        type=PricingRuleType.PERCENTAGE,
        parameters={
            "value": "10",
        },
    )

    fixed_amount_rule = PricingRuleTable(
        name="Pricing Test - Fixed 20",
        description="Descuento fijo de S/20",
        type=PricingRuleType.FIXED_AMOUNT,
        parameters={
            "value": "20.00",
        },
    )

    db_session.add_all([
        percentage_rule,
        fixed_amount_rule,
    ])
    await db_session.commit()

    await db_session.refresh(percentage_rule)
    await db_session.refresh(fixed_amount_rule)

    # ---------------------------------------------------------
    # Promotion -> Pricing rule
    # ---------------------------------------------------------

    promotion_pricing_rules = [
        PromotionPricingRuleTable(
            promotion_id=promotion_1.id,
            pricing_rule_id=percentage_rule.id,
            execution_order=0,
        ),
        PromotionPricingRuleTable(
            promotion_id=promotion_2.id,
            pricing_rule_id=fixed_amount_rule.id,
            execution_order=0,
        ),
    ]

    db_session.add_all(promotion_pricing_rules)
    await db_session.commit()

    # ---------------------------------------------------------
    # Targets
    # ---------------------------------------------------------

    targets = [
        PromotionTargetTable(
            promotion_id=promotion_1.id,
            target_type=PromotionTargetType.PRODUCT,
            reference_id=products[0].id,
        ),
        PromotionTargetTable(
            promotion_id=promotion_2.id,
            target_type=PromotionTargetType.PRODUCT,
            reference_id=products[1].id,
        ),
    ]

    db_session.add_all(targets)
    await db_session.commit()

    # ---------------------------------------------------------
    # Audiences
    # ---------------------------------------------------------

    audiences = [
        PromotionAudienceTable(
            promotion_id=promotion_1.id,
            audience_type=PromotionAudienceType.ALL_CUSTOMERS,
        ),
        PromotionAudienceTable(
            promotion_id=promotion_2.id,
            audience_type=PromotionAudienceType.CUSTOMER_GROUP,
            reference_value="WHOLESALE",
        ),
    ]

    db_session.add_all(audiences)
    await db_session.commit()

    # ---------------------------------------------------------
    # Condition
    # ---------------------------------------------------------

    condition = PromotionConditionTable(
        promotion_id=promotion_2.id,
        condition_type=PromotionConditionType.PAYMENT_METHOD,
        parameters={
            "payment_method": "YAPE",
        },
        description="Aplica únicamente pagando con Yape",
    )

    db_session.add(condition)
    await db_session.commit()

    return {
        "promotions": [promotion_1, promotion_2],
        "percentage_rule": percentage_rule,
        "fixed_amount_rule": fixed_amount_rule,
        "promotion_pricing_rules": promotion_pricing_rules,
        "targets": targets,
        "audiences": audiences,
        "condition": condition,
    }