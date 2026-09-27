from datetime import datetime, timezone
from decimal import Decimal

import pytest

pytestmark = pytest.mark.asyncio(
    loop_scope="session",
)

from app.features.sales.types.sale import SaleChannel
from app.features.products.types import CategoryType
from app.features.pricing.types.promotion_types import PromotionConditionType
from tests.helpers.create_test_promotion import create_cart_condition_promotion
from app.features.pricing.dtos.cart_pricing_dto import CartPricingContext, CartPricingItemDTO
from tests.helpers.create_order_subtotal_promotion import create_order_subtotal_promotion
from app.features.pricing.types.promotion_types import (
    PromotionStackingMode,
)

from tests.helpers.create_per_item_promotion import (
    create_per_item_promotion,
)

from app.features.pricing.types.pricing_rules_types import (
    PricingRuleType,
)

async def test_order_subtotal_percentage_applies_once_to_order_subtotal(
    db_session,
    cart_pricing_service,
    pricing_products,
):
    polo = pricing_products["products"][0]   # S/50
    jean = pricing_products["products"][1]  # S/100

    variant_sizes = pricing_products["variant_sizes"]

    polo_size = variant_sizes[0]
    jean_size = variant_sizes[2]

    await create_order_subtotal_promotion(
        db_session,
        product_ids=[
            polo.id,
            jean.id,
        ],
        rule_type=PricingRuleType.PERCENTAGE,
        rule_parameters={
            "percentage": "10",
        },
    )

    context = CartPricingContext(
        items=[
            CartPricingItemDTO(
                item_id=polo_size.id,
                product_id=polo.id,
                category=polo.category,
                brand=polo.brand,
                quantity=1,
                unit_price=polo.base_price,
            ),
            CartPricingItemDTO(
                item_id=jean_size.id,
                product_id=jean.id,
                category=jean.category,
                brand=jean.brand,
                quantity=1,
                unit_price=jean.base_price,
            ),
        ],
        sale_channel=SaleChannel.ECOMMERCE,
        customer_id=None,
        customer_type=None,
        now=datetime.now(timezone.utc),
    )

    result = await cart_pricing_service.calculate(
        context=context,
    )

    assert result.subtotal == Decimal("150.00")
    assert result.discount_amount == Decimal("15.00")
    assert result.total == Decimal("135.00")

    assert len(result.applied_promotions) == 1
    assert (
        result.applied_promotions[0].discount_amount
        == Decimal("15.00")
    )


async def test_order_subtotal_fixed_amount_applies_once_to_order_subtotal(
    db_session,
    cart_pricing_service,
    pricing_products,
):
    polo = pricing_products["products"][0]      # S/50
    jean = pricing_products["products"][1]     # S/100
    casaca = pricing_products["products"][2]   # S/150

    variant_sizes = pricing_products["variant_sizes"]

    polo_size = variant_sizes[0]
    jean_size = variant_sizes[2]
    casaca_size = variant_sizes[4]

    await create_order_subtotal_promotion(
        db_session,
        product_ids=[
            polo.id,
            jean.id,
            casaca.id,
        ],
        rule_type=PricingRuleType.FIXED_AMOUNT,
        rule_parameters={
            "amount": "30.00",
        },
    )

    context = CartPricingContext(
        items=[
            CartPricingItemDTO(
                item_id=polo_size.id,
                product_id=polo.id,
                category=polo.category,
                brand=polo.brand,
                quantity=1,
                unit_price=polo.base_price,
            ),
            CartPricingItemDTO(
                item_id=jean_size.id,
                product_id=jean.id,
                category=jean.category,
                brand=jean.brand,
                quantity=1,
                unit_price=jean.base_price,
            ),
            CartPricingItemDTO(
                item_id=casaca_size.id,
                product_id=casaca.id,
                category=casaca.category,
                brand=casaca.brand,
                quantity=1,
                unit_price=casaca.base_price,
            ),
        ],
        sale_channel=SaleChannel.ECOMMERCE,
        customer_id=None,
        customer_type=None,
        now=datetime.now(timezone.utc),
    )

    result = await cart_pricing_service.calculate(
        context=context,
    )

    assert result.subtotal == Decimal("300.00")
    assert result.discount_amount == Decimal("30.00")
    assert result.total == Decimal("270.00")

    assert len(result.applied_promotions) == 1
    assert (
        result.applied_promotions[0].discount_amount
        == Decimal("30.00")
    )



async def test_cart_pricing_recalculates_when_quantity_changes(
    db_session,
    cart_pricing_service,
    pricing_products,
):
    jean = pricing_products["products"][1]  # S/100
    jean_size = pricing_products["variant_sizes"][2]

    await create_cart_condition_promotion(
        db_session,
        category=CategoryType.PANT,
        condition_type=PromotionConditionType.MINIMUM_ORDER_AMOUNT,
        parameters={
            "minimum_amount": "300.00",
        },
        discount="10",
    )

    def build_context(quantity: int):
        return CartPricingContext(
            items=[
                CartPricingItemDTO(
                    item_id=jean_size.id,
                    product_id=jean.id,
                    category=jean.category,
                    brand=jean.brand,
                    quantity=quantity,
                    unit_price=jean.base_price,
                )
            ],
            sale_channel=SaleChannel.ECOMMERCE,
            customer_id=None,
            customer_type=None,
            now=datetime.now(timezone.utc),
        )

    result = await cart_pricing_service.calculate(
        context=build_context(2),
    )

    assert result.subtotal == Decimal("200.00")
    assert result.discount_amount == Decimal("0.00")
    assert result.total == Decimal("200.00")

    result = await cart_pricing_service.calculate(
        context=build_context(3),
    )

    assert result.subtotal == Decimal("300.00")
    assert result.discount_amount == Decimal("30.00")
    assert result.total == Decimal("270.00")

    result = await cart_pricing_service.calculate(
        context=build_context(2),
    )

    assert result.subtotal == Decimal("200.00")
    assert result.discount_amount == Decimal("0.00")
    assert result.total == Decimal("200.00")

async def test_per_item_stackable_then_order_subtotal_stackable(
    db_session,
    cart_pricing_service,
    pricing_products,
):
    polo = pricing_products["products"][0]   # S/50
    jean = pricing_products["products"][1]  # S/100

    variant_sizes = pricing_products["variant_sizes"]

    polo_size = variant_sizes[0]
    jean_size = variant_sizes[2]

    # PER_ITEM -> 10% solamente sobre el polo
    await create_per_item_promotion(
        db_session,
        product_ids=[
            polo.id,
        ],
        rule_type=PricingRuleType.PERCENTAGE,
        rule_parameters={
            "percentage": "10",
        },
        name="Per Item Polo 10%",
        stacking_mode=PromotionStackingMode.STACKABLE,
        priority=10,
    )

    # ORDER_SUBTOTAL -> S/20 después de aplicar PER_ITEM
    await create_order_subtotal_promotion(
        db_session,
        product_ids=[
            polo.id,
            jean.id,
        ],
        rule_type=PricingRuleType.FIXED_AMOUNT,
        rule_parameters={
            "amount": "20.00",
        },
        name="Order Subtotal S/20",
        stacking_mode=PromotionStackingMode.STACKABLE,
        priority=10,
    )

    context = CartPricingContext(
        items=[
            CartPricingItemDTO(
                item_id=polo_size.id,
                product_id=polo.id,
                category=polo.category,
                brand=polo.brand,
                quantity=1,
                unit_price=polo.base_price,
            ),
            CartPricingItemDTO(
                item_id=jean_size.id,
                product_id=jean.id,
                category=jean.category,
                brand=jean.brand,
                quantity=1,
                unit_price=jean.base_price,
            ),
        ],
        sale_channel=SaleChannel.ECOMMERCE,
        customer_id=None,
        customer_type=None,
        now=datetime.now(timezone.utc),
    )

    result = await cart_pricing_service.calculate(
        context=context,
    )

    assert result.subtotal == Decimal("150.00")

    polo_result = next(
        item
        for item in result.items
        if item.product_id == polo.id
    )

    jean_result = next(
        item
        for item in result.items
        if item.product_id == jean.id
    )

    assert polo_result.original_total == Decimal("50.00")
    assert polo_result.final_total == Decimal("45.00")
    assert polo_result.discount_amount == Decimal("5.00")

    assert jean_result.original_total == Decimal("100.00")
    assert jean_result.final_total == Decimal("100.00")
    assert jean_result.discount_amount == Decimal("0.00")

    # 150
    # - 5 PER_ITEM
    # - 20 ORDER_SUBTOTAL
    # = 125

    assert result.discount_amount == Decimal("25.00")
    assert result.total == Decimal("125.00")

    assert len(result.applied_promotions) == 2

async def test_order_subtotal_exclusive_wins_over_other_promotions(
    db_session,
    cart_pricing_service,
    pricing_products,
):
    polo = pricing_products["products"][0]   # S/50
    jean = pricing_products["products"][1]  # S/100

    variant_sizes = pricing_products["variant_sizes"]

    polo_size = variant_sizes[0]
    jean_size = variant_sizes[2]

    # ORDER_SUBTOTAL stackable menor prioridad
    await create_order_subtotal_promotion(
        db_session,
        product_ids=[
            polo.id,
            jean.id,
        ],
        rule_type=PricingRuleType.FIXED_AMOUNT,
        rule_parameters={
            "amount": "10.00",
        },
        name="Stackable S/10",
        stacking_mode=PromotionStackingMode.STACKABLE,
        priority=5,
    )

    # ORDER_SUBTOTAL exclusive mayor prioridad
    await create_order_subtotal_promotion(
        db_session,
        product_ids=[
            polo.id,
            jean.id,
        ],
        rule_type=PricingRuleType.FIXED_AMOUNT,
        rule_parameters={
            "amount": "30.00",
        },
        name="Exclusive S/30",
        stacking_mode=PromotionStackingMode.EXCLUSIVE,
        priority=20,
    )

    context = CartPricingContext(
        items=[
            CartPricingItemDTO(
                item_id=polo_size.id,
                product_id=polo.id,
                category=polo.category,
                brand=polo.brand,
                quantity=1,
                unit_price=polo.base_price,
            ),
            CartPricingItemDTO(
                item_id=jean_size.id,
                product_id=jean.id,
                category=jean.category,
                brand=jean.brand,
                quantity=1,
                unit_price=jean.base_price,
            ),
        ],
        sale_channel=SaleChannel.ECOMMERCE,
        customer_id=None,
        customer_type=None,
        now=datetime.now(timezone.utc),
    )

    result = await cart_pricing_service.calculate(
        context=context,
    )

    assert result.subtotal == Decimal("150.00")

    # Solo debe sobrevivir la EXCLUSIVE de S/30
    assert result.discount_amount == Decimal("30.00")
    assert result.total == Decimal("120.00")

    assert len(result.applied_promotions) == 1

    applied = result.applied_promotions[0]

    assert applied.name == "Exclusive S/30"
    assert applied.discount_amount == Decimal("30.00")

async def test_per_item_exclusive_wins_over_order_subtotal(
    db_session,
    cart_pricing_service,
    pricing_products,
):
    polo = pricing_products["products"][0]   # S/50
    jean = pricing_products["products"][1]  # S/100

    variant_sizes = pricing_products["variant_sizes"]

    polo_size = variant_sizes[0]
    jean_size = variant_sizes[2]

    # PER_ITEM EXCLUSIVE -> 10% sobre el polo
    await create_per_item_promotion(
        db_session,
        product_ids=[
            polo.id,
        ],
        rule_type=PricingRuleType.PERCENTAGE,
        rule_parameters={
            "percentage": "10",
        },
        name="Exclusive Polo 10%",
        stacking_mode=PromotionStackingMode.EXCLUSIVE,
        priority=20,
    )

    # ORDER_SUBTOTAL STACKABLE -> S/20
    await create_order_subtotal_promotion(
        db_session,
        product_ids=[
            polo.id,
            jean.id,
        ],
        rule_type=PricingRuleType.FIXED_AMOUNT,
        rule_parameters={
            "amount": "20.00",
        },
        name="Order Subtotal S/20",
        stacking_mode=PromotionStackingMode.STACKABLE,
        priority=10,
    )

    context = CartPricingContext(
        items=[
            CartPricingItemDTO(
                item_id=polo_size.id,
                product_id=polo.id,
                category=polo.category,
                brand=polo.brand,
                quantity=1,
                unit_price=polo.base_price,
            ),
            CartPricingItemDTO(
                item_id=jean_size.id,
                product_id=jean.id,
                category=jean.category,
                brand=jean.brand,
                quantity=1,
                unit_price=jean.base_price,
            ),
        ],
        sale_channel=SaleChannel.ECOMMERCE,
        customer_id=None,
        customer_type=None,
        now=datetime.now(timezone.utc),
    )

    result = await cart_pricing_service.calculate(
        context=context,
    )

    assert result.subtotal == Decimal("150.00")

    # PER_ITEM EXCLUSIVE:
    # Polo 50 -> 45
    # Jean 100
    #
    # Subtotal después de PER_ITEM = 145
    #
    # ORDER_SUBTOTAL STACKABLE:
    # 145 - 20 = 125
    #
    # Descuento total = 5 + 20 = 25

    assert result.discount_amount == Decimal("25.00")
    assert result.total == Decimal("125.00")

    assert len(result.applied_promotions) == 2

    promotions = {
        promotion.name: promotion
        for promotion in result.applied_promotions
    }

    assert promotions["Exclusive Polo 10%"].discount_amount == Decimal("5.00")
    assert promotions["Order Subtotal S/20"].discount_amount == Decimal("20.00")

async def test_order_subtotal_uses_full_quantity_total(
    db_session,
    cart_pricing_service,
    pricing_products,
):
    jean = pricing_products["products"][1]  # S/100
    jean_size = pricing_products["variant_sizes"][2]

    await create_order_subtotal_promotion(
        db_session,
        product_ids=[
            jean.id,
        ],
        rule_type=PricingRuleType.PERCENTAGE,
        rule_parameters={
            "percentage": "10",
        },
        name="Order Subtotal 10%",
        stacking_mode=PromotionStackingMode.STACKABLE,
        priority=10,
    )

    context = CartPricingContext(
        items=[
            CartPricingItemDTO(
                item_id=jean_size.id,
                product_id=jean.id,
                category=jean.category,
                brand=jean.brand,
                quantity=3,
                unit_price=jean.base_price,
            ),
        ],
        sale_channel=SaleChannel.ECOMMERCE,
        customer_id=None,
        customer_type=None,
        now=datetime.now(timezone.utc),
    )

    result = await cart_pricing_service.calculate(
        context=context,
    )

    # 100 × 3
    assert result.subtotal == Decimal("300.00")

    # 10% de 300, no de 100
    assert result.discount_amount == Decimal("30.00")
    assert result.total == Decimal("270.00")

    assert len(result.applied_promotions) == 1
    assert (
        result.applied_promotions[0].discount_amount
        == Decimal("30.00")
    )

async def test_order_subtotal_discount_cannot_make_total_negative(
    db_session,
    cart_pricing_service,
    pricing_products,
):
    polo = pricing_products["products"][0]
    polo_size = pricing_products["variant_sizes"][0]

    await create_order_subtotal_promotion(
        db_session,
        product_ids=[
            polo.id,
        ],
        rule_type=PricingRuleType.FIXED_AMOUNT,
        rule_parameters={
            "amount": "50.00",
        },
        name="Order Subtotal S/50",
        stacking_mode=PromotionStackingMode.STACKABLE,
        priority=10,
    )

    context = CartPricingContext(
        items=[
            CartPricingItemDTO(
                item_id=polo_size.id,
                product_id=polo.id,
                category=polo.category,
                brand=polo.brand,
                quantity=1,
                unit_price=Decimal("20.00"),
            ),
        ],
        sale_channel=SaleChannel.ECOMMERCE,
        customer_id=None,
        customer_type=None,
        now=datetime.now(timezone.utc),
    )

    result = await cart_pricing_service.calculate(
        context=context,
    )

    assert result.subtotal == Decimal("20.00")

    # FIXED_AMOUNT usa min(50, 20)
    assert result.discount_amount == Decimal("20.00")

    assert result.total == Decimal("0.00")

    assert len(result.applied_promotions) == 1
    assert (
        result.applied_promotions[0].discount_amount
        == Decimal("20.00")
    )