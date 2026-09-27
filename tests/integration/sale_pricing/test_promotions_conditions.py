from datetime import datetime, timezone, timedelta
from decimal import Decimal

from app.features.pricing.models.promotion_pricing_rule import PromotionPricingRuleTable
from app.features.pricing.dtos.sale_pricing import (
    PricingItemDTO,
    SalePricingContext,
)
from tests.helpers.create_test_promotion import create_test_promotion
from app.features.sales.types.customer import CustomerType
from app.features.pricing.types.pricing_rules_types import PricingRuleType
from app.features.sales.types.sale import SaleChannel
from app.features.pricing.models.model_pricing_rule import PricingRuleTable
from app.features.pricing.models.model_promotion import PromotionTable
from app.features.pricing.models.promotion_audience import (
    PromotionAudienceTable,
)
from app.features.pricing.models.promotion_target import (
    PromotionTargetTable,
)
from app.features.pricing.types.promotion_types import (
    PromotionAudienceType,
    PromotionStackingMode,
    PromotionTargetType,
)
from app.core.exceptions import ValidationError

import pytest

pytestmark = pytest.mark.asyncio(
    loop_scope="session",
)



async def test_calculate_exclusive_promotion_blocks_stackable_promotion(
    db_session,
    sale_pricing_service,
    pricing_products,
    pricing_promotions,
    pricing_customer,
):
    products = pricing_products["products"]
    customer = pricing_customer

    # ---------------------------------------------------------
    # Promotion 3 - S/20 OFF - EXCLUSIVE
    # Compite con promotion_1 sobre el mismo producto.
    # ---------------------------------------------------------

    promotion_3 = PromotionTable(
        name="Pricing Test - Exclusive S/20 OFF",
        description="Promoción exclusiva que bloquea otras promociones",
        sales_channel=SaleChannel.ECOMMERCE,
        stacking_mode=PromotionStackingMode.EXCLUSIVE,
        priority=20,
        starts_at=datetime.now(timezone.utc),
        ends_at=None,
        is_active=True,
    )

    db_session.add(promotion_3)
    await db_session.commit()
    await db_session.refresh(promotion_3)

    # ---------------------------------------------------------
    # Pricing rule
    # ---------------------------------------------------------

    fixed_amount_rule = PricingRuleTable(
        name="Pricing Test - Exclusive Fixed 20",
        description="Descuento fijo exclusivo de S/20",
        type=PricingRuleType.FIXED_AMOUNT,
        parameters={
            "amount": "20.00",
        },
    )

    db_session.add(fixed_amount_rule)
    await db_session.commit()
    await db_session.refresh(fixed_amount_rule)

    # ---------------------------------------------------------
    # Promotion -> Pricing rule
    # ---------------------------------------------------------

    promotion_pricing_rule = PromotionPricingRuleTable(
        promotion_id=promotion_3.id,
        pricing_rule_id=fixed_amount_rule.id,
        execution_order=0,
    )

    db_session.add(promotion_pricing_rule)
    await db_session.commit()

    # ---------------------------------------------------------
    # Target -> mismo producto de promotion_1
    # ---------------------------------------------------------

    target = PromotionTargetTable(
        promotion_id=promotion_3.id,
        target_type=PromotionTargetType.PRODUCT,
        reference_id=products[0].id,
    )

    db_session.add(target)
    await db_session.commit()

    # ---------------------------------------------------------
    # Audience -> todos los clientes
    # ---------------------------------------------------------

    audience = PromotionAudienceTable(
        promotion_id=promotion_3.id,
        audience_type=PromotionAudienceType.ALL_CUSTOMERS,
    )

    db_session.add(audience)
    await db_session.commit()

    # ---------------------------------------------------------
    # Pricing context
    # ---------------------------------------------------------

    context = SalePricingContext(
        items=[
            PricingItemDTO(
                product_id=products[0].id,
                quantity=2,
                category=products[0].category,
                brand=products[0].brand,
                unit_price=products[0].base_price,
            ),
        ],
        sale_channel=SaleChannel.ECOMMERCE,
        customer_id=customer.id,
        customer_type=CustomerType.REGULAR,
        coupon_code=None,
        now=datetime.now(timezone.utc),
        shipping_cost=Decimal("15.00"),
    )

    # ---------------------------------------------------------
    # Calculate
    # ---------------------------------------------------------

    result = await sale_pricing_service.calculate(
        context=context,
    )

    assert len(result.items) == 1

    polo_result = result.items[0]

    # ---------------------------------------------------------
    # Polo: 2 x S/50
    #
    # Promotion 1 = 10% STACKABLE
    # Promotion 3 = S/20 EXCLUSIVE
    #
    # La exclusiva bloquea a la stackable.
    # ---------------------------------------------------------

    assert polo_result.quantity == 2
    assert polo_result.original_unit_price == Decimal("50.00")

    assert polo_result.final_unit_price == Decimal("30.00")
    assert polo_result.original_total == Decimal("100.00")
    assert polo_result.final_total == Decimal("60.00")
    assert polo_result.discount_amount == Decimal("40.00")

    # ---------------------------------------------------------
    # Sale totals
    # ---------------------------------------------------------

    assert result.subtotal == Decimal("100.00")
    assert result.discount_amount == Decimal("40.00")
    assert result.shipping_cost == Decimal("15.00")
    assert result.total == Decimal("75.00")


async def test_calculate_applies_oldest_exclusive_promotion_when_priority_is_equal(
    db_session,
    sale_pricing_service,
    pricing_products,
    pricing_promotions,
    pricing_customer,
):
    products = pricing_products["products"]
    promotion_old = pricing_promotions["promotions"][1]
    customer = pricing_customer

    # ---------------------------------------------------------
    # Promotion 1 - ya viene de la fixture
    #
    # STACKABLE
    # priority = 10
    # 10% OFF
    # ---------------------------------------------------------

    promotion_old.created_at = datetime.now(timezone.utc) - timedelta(days=2)

    # ---------------------------------------------------------
    # Promotion 3 - misma prioridad, pero más reciente
    #
    # STACKABLE
    # priority = 10
    # 20% OFF
    # ---------------------------------------------------------

    promotion_3 = PromotionTable(
        name="Pricing Test - 20% OFF",
        description="Promoción más reciente con misma prioridad",
        sales_channel=SaleChannel.ECOMMERCE,
        stacking_mode=PromotionStackingMode.EXCLUSIVE,
        priority=10,
        starts_at=datetime.now(timezone.utc),
        ends_at=None,
        is_active=True,
        created_at=datetime.now(timezone.utc),
    )

    db_session.add(promotion_3)
    await db_session.commit()
    await db_session.refresh(promotion_3)

    # ---------------------------------------------------------
    # Pricing rule
    # ---------------------------------------------------------

    percentage_rule = PricingRuleTable(
        name="Pricing Test - 20 Percent",
        description="Descuento porcentual del 20%",
        type=PricingRuleType.PERCENTAGE,
        parameters={
            "percentage": "20",
        },
    )

    db_session.add(percentage_rule)
    await db_session.commit()
    await db_session.refresh(percentage_rule)

    # ---------------------------------------------------------
    # Promotion -> Pricing rule
    # ---------------------------------------------------------

    promotion_pricing_rule = PromotionPricingRuleTable(
        promotion_id=promotion_3.id,
        pricing_rule_id=percentage_rule.id,
        execution_order=0,
    )

    db_session.add(promotion_pricing_rule)
    await db_session.commit()

    # ---------------------------------------------------------
    # Target -> mismo producto de promotion_old
    # ---------------------------------------------------------

    target = PromotionTargetTable(
        promotion_id=promotion_3.id,
        target_type=PromotionTargetType.PRODUCT,
        reference_id=products[0].id,
    )

    db_session.add(target)
    await db_session.commit()

    # ---------------------------------------------------------
    # Audience
    # ---------------------------------------------------------

    audience = PromotionAudienceTable(
        promotion_id=promotion_3.id,
        audience_type=PromotionAudienceType.ALL_CUSTOMERS,
    )

    db_session.add(audience)
    await db_session.commit()

    # ---------------------------------------------------------
    # Pricing context
    # ---------------------------------------------------------

    context = SalePricingContext(
        items=[
            PricingItemDTO(
                product_id=products[0].id,
                quantity=2,
                category=products[0].category,
                brand=products[0].brand,
                unit_price=products[0].base_price,
            ),
        ],
        sale_channel=SaleChannel.ECOMMERCE,
        customer_id=customer.id,
        customer_type=CustomerType.REGULAR,
        coupon_code=None,
        now=datetime.now(timezone.utc),
        shipping_cost=Decimal("15.00"),
    )

    # ---------------------------------------------------------
    # Calculate
    # ---------------------------------------------------------

    result = await sale_pricing_service.calculate(
        context=context,
    )

    assert len(result.items) == 1

    polo_result = result.items[0]

    # ---------------------------------------------------------
    # Priority
    #
    # Ambas promociones:
    #   EXCLUSIVE
    #   priority = 10
    #
    # Promotion 2 es más antigua que Promotion 3.
    # Por lo tanto, Promotion 2 gana el desempate.
    #
    # Promotion 2 aplica S/20 de descuento total.
    # ---------------------------------------------------------

    assert polo_result.quantity == 2
    assert polo_result.original_unit_price == Decimal("50.00")
    assert polo_result.final_unit_price == Decimal("40.00")
    assert polo_result.original_total == Decimal("100.00")
    assert polo_result.final_total == Decimal("80.00")
    assert polo_result.discount_amount == Decimal("20.00")

    # ---------------------------------------------------------
    # Sale totals
    # ---------------------------------------------------------

    assert result.subtotal == Decimal("100.00")
    assert result.discount_amount == Decimal("20.00")
    assert result.shipping_cost == Decimal("15.00")
    assert result.total == Decimal("95.00")


async def test_calculate_rejects_promotion_before_start_date(
    db_session,
    sale_pricing_service,
    pricing_products,
):
    product = pricing_products["products"][0]
    now = datetime.now(timezone.utc)

    await create_test_promotion(
        db_session,
        product_id=product.id,
        starts_at=now + timedelta(days=1),
        ends_at=None,
    )

    context = SalePricingContext(
        items=[
            PricingItemDTO(
                product_id=product.id,
                quantity=2,
                category=product.category,
                brand=product.brand,
                unit_price=Decimal("50.00"),
            )
        ],
        sale_channel=SaleChannel.ECOMMERCE,
        now=now,
    )

    with pytest.raises(
        ValidationError,
        match="La promoción aún no está disponible.",
    ):
        await sale_pricing_service.calculate(context=context)


async def test_calculate_rejects_expired_promotion(
    db_session,
    sale_pricing_service,
    pricing_products,
):
    product = pricing_products["products"][0]
    now = datetime.now(timezone.utc)

    await create_test_promotion(
        db_session,
        product_id=product.id,
        starts_at=now - timedelta(days=2),
        ends_at=now - timedelta(days=1),
    )

    context = SalePricingContext(
        items=[
            PricingItemDTO(
                product_id=product.id,
                quantity=2,
                category=product.category,
                brand=product.brand,
                unit_price=Decimal("50.00"),
            )
        ],
        sale_channel=SaleChannel.ECOMMERCE,
        now=now,
    )

    with pytest.raises(
        ValidationError,
        match="La promocion ha expirado",
    ):
        await sale_pricing_service.calculate(context=context)