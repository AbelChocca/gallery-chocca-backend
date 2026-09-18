from datetime import datetime, timezone
from decimal import Decimal

import pytest

from app.features.sales.types.sale import SaleChannel
from app.features.sales.types.customer import CustomerType
from app.features.products.types import CategoryType
from app.features.pricing.types.promotion_types import PromotionConditionType
from tests.helpers.create_test_promotion import create_cart_condition_promotion
from app.features.pricing.dtos.cart_pricing_dto import CartPricingContext, CartPricingItemDTO


@pytest.mark.asyncio
async def test_cart_pricing_recalculates_when_quantity_changes(
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

    # GET cart -> x2
    result = await cart_pricing_service.calculate(
        context=build_context(2),
    )

    assert result.subtotal == Decimal("200.00")
    assert result.discount_amount == Decimal("0.00")
    assert result.total == Decimal("200.00")

    # PATCH quantity = 3
    result = await cart_pricing_service.calculate(
        context=build_context(3),
    )

    assert result.subtotal == Decimal("300.00")
    assert result.discount_amount == Decimal("30.00")
    assert result.total == Decimal("270.00")

    # PATCH quantity = 2
    result = await cart_pricing_service.calculate(
        context=build_context(2),
    )

    assert result.subtotal == Decimal("200.00")
    assert result.discount_amount == Decimal("0.00")
    assert result.total == Decimal("200.00")