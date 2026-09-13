from datetime import datetime, timezone
from decimal import Decimal

import pytest

from app.features.pricing.models.coupon import CouponTable
from app.features.pricing.dtos.sale_pricing import (
    PricingItemDTO,
    SalePricingContext,
)
from app.features.sales.types.customer import CustomerType
from app.features.sales.types.sale import SaleChannel


@pytest.mark.asyncio
async def test_calculate_applies_coupon_promotion_to_customer_cart(
    db_session,
    sale_pricing_service,
    pricing_products,
    pricing_promotions,
    pricing_customer,
):
    products = pricing_products["products"]
    promotion_1 = pricing_promotions["promotions"][0]
    customer = pricing_customer

    coupon = CouponTable(
        promotion_id=promotion_1.id,
        code="PRICING10",
        is_active=True,
        starts_at=None,
        ends_at=None,
        max_redemptions=100,
        max_redemptions_per_customer=1,
        used_count=0,
    )

    db_session.add(coupon)
    await db_session.commit()
    await db_session.refresh(coupon)

    now = datetime.now(timezone.utc)

    context = SalePricingContext(
        items=[
            PricingItemDTO(
                product_id=products[0].id,
                quantity=2,
                category=products[0].category,
                brand=products[0].brand,
                unit_price=products[0].base_price,
            ),
            PricingItemDTO(
                product_id=products[1].id,
                quantity=1,
                category=products[1].category,
                brand=products[1].brand,
                unit_price=products[1].base_price,
            ),
        ],
        sale_channel=SaleChannel.ECOMMERCE,
        customer_id=customer.id,
        customer_type=CustomerType.REGULAR,
        coupon_code=coupon.code,
        now=now,
        shipping_cost=Decimal("15.00"),
    )

    result = await sale_pricing_service.calculate(
        context=context,
    )

    assert len(result.items) == 2

    # ---------------------------------------------------------
    # Polo: 2 x S/50 -> 10% OFF
    # ---------------------------------------------------------

    polo_result = next(
        item
        for item in result.items
        if item.product_id == products[0].id
    )

    assert polo_result.quantity == 2
    assert polo_result.original_unit_price == Decimal("50.00")
    assert polo_result.final_unit_price == Decimal("45.00")
    assert polo_result.original_total == Decimal("100.00")
    assert polo_result.final_total == Decimal("90.00")
    assert polo_result.discount_amount == Decimal("10.00")

    # ---------------------------------------------------------
    # Jean: 1 x S/100 -> no discount
    # ---------------------------------------------------------

    jean_result = next(
        item
        for item in result.items
        if item.product_id == products[1].id
    )

    assert jean_result.quantity == 1
    assert jean_result.original_unit_price == Decimal("100.00")
    assert jean_result.final_unit_price == Decimal("100.00")
    assert jean_result.original_total == Decimal("100.00")
    assert jean_result.final_total == Decimal("100.00")
    assert jean_result.discount_amount == Decimal("0.00")

    # ---------------------------------------------------------
    # Sale totals
    # ---------------------------------------------------------

    assert result.subtotal == Decimal("200.00")
    assert result.discount_amount == Decimal("10.00")
    assert result.shipping_cost == Decimal("15.00")
    assert result.total == Decimal("205.00")