from datetime import datetime, timezone
from decimal import Decimal

import pytest

from app.features.sales.types.sale import SaleChannel
from app.features.sales.types.customer import CustomerType
from app.features.products.types import CategoryType
from app.features.pricing.types.promotion_types import PromotionConditionType, PromotionAudienceType
from tests.helpers.create_test_promotion import create_cart_condition_promotion, create_category_audience_promotion
from app.features.pricing.dtos.cart_pricing_dto import CartPricingContext, CartPricingItemDTO

@pytest.mark.asyncio
async def test_cart_pricing_applies_minimum_order_amount_condition(
    db_session,
    cart_pricing_service,
    pricing_products,
):
    jean = pricing_products["products"][1]  # S/100

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

    # S/200 -> no cumple
    result = await cart_pricing_service.calculate(
        context=build_context(2),
    )

    assert result.subtotal == Decimal("200.00")
    assert result.discount_amount == Decimal("0.00")
    assert result.total == Decimal("200.00")

    # S/300 -> cumple
    result = await cart_pricing_service.calculate(
        context=build_context(3),
    )

    assert result.subtotal == Decimal("300.00")
    assert result.discount_amount == Decimal("30.00")
    assert result.total == Decimal("270.00")

@pytest.mark.asyncio
async def test_cart_pricing_respects_customer_audience(
    db_session,
    cart_pricing_service,
    pricing_products,
    pricing_customer,
):
    pant = pricing_products["products"][0]
    customer = pricing_customer

    await create_category_audience_promotion(
        db_session,
        category=CategoryType.PANT,
        audience_type=PromotionAudienceType.CUSTOMER,
        reference_id=customer.id,
        discount="10",
    )

    def build_context(
        customer_id: int | None,
        customer_type: CustomerType | None,
    ):
        return CartPricingContext(
            items=[
                CartPricingItemDTO(
                    product_id=pant.id,
                    category=pant.category,
                    brand=pant.brand,
                    quantity=2,
                    unit_price=pant.base_price,
                )
            ],
            sale_channel=SaleChannel.ECOMMERCE,
            customer_id=customer_id,
            customer_type=customer_type,
            now=datetime.now(timezone.utc),
        )

    eligible = await cart_pricing_service.calculate(
        context=build_context(
            customer.id,
            customer.customer_type,
        )
    )

    not_eligible = await cart_pricing_service.calculate(
        context=build_context(
            999999,
            CustomerType.REGULAR,
        )
    )

    assert eligible.total == Decimal("90.00")
    assert eligible.discount_amount == Decimal("10.00")

    assert not_eligible.total == Decimal("100.00")
    assert not_eligible.discount_amount == Decimal("0.00")