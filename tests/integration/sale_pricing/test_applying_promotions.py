from datetime import datetime, timezone
from decimal import Decimal

import pytest

pytestmark = pytest.mark.asyncio(
    loop_scope="session",
)

from app.features.pricing.models.coupon import CouponTable
from app.features.pricing.dtos.sale_pricing import (
    PricingItemDTO,
    SalePricingContext,
)
from app.features.sales.types.customer import CustomerType
from app.features.sales.types.sale import SaleChannel
from app.features.products.types import CategoryType, BrandType, FitType
from app.features.products.models.model_product import ProductTable
from tests.helpers.create_test_promotion import create_category_target_promotion



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


async def test_calculate_applies_category_promotion_only_to_target_category(
    db_session,
    sale_pricing_service,
    pricing_products,
    pricing_customer,
):
    products = pricing_products["products"]
    pant = products[0]

    short = ProductTable(
        nombre="Short Pricing Test",
        descripcion="Short fuera del target de la promoción",
        brand=BrandType.BGOO,
        category=CategoryType.SHORT,
        fit=FitType.REGULAR,
        slug="pricing-short-category-target-test",
        base_price=Decimal("100.00"),
    )

    db_session.add(short)
    await db_session.commit()
    await db_session.refresh(short)

    await create_category_target_promotion(
        db_session,
        category=CategoryType.PANT,
        discount="10",
    )

    customer = pricing_customer

    context = SalePricingContext(
        items=[
            PricingItemDTO(
                product_id=pant.id,
                quantity=1,
                category=pant.category,
                brand=pant.brand,
                unit_price=pant.base_price,
            ),
            PricingItemDTO(
                product_id=short.id,
                quantity=1,
                category=short.category,
                brand=short.brand,
                unit_price=short.base_price,
            ),
        ],
        sale_channel=SaleChannel.ECOMMERCE,
        customer_id=customer.id,
        customer_type=CustomerType.REGULAR,
        now=datetime.now(timezone.utc),
        shipping_cost=Decimal("0.00"),
    )

    result = await sale_pricing_service.calculate(
        context=context,
    )

    assert len(result.items) == 2

    # ---------------------------------------------------------
    # PANT: S/50 -> 10% OFF
    # ---------------------------------------------------------

    pant_result = next(
        item
        for item in result.items
        if item.product_id == pant.id
    )

    assert pant_result.original_unit_price == Decimal("50.00")
    assert pant_result.final_unit_price == Decimal("45.00")
    assert pant_result.original_total == Decimal("50.00")
    assert pant_result.final_total == Decimal("45.00")
    assert pant_result.discount_amount == Decimal("5.00")

    # ---------------------------------------------------------
    # SHORT: S/100 -> no discount
    # ---------------------------------------------------------

    short_result = next(
        item
        for item in result.items
        if item.product_id == short.id
    )

    assert short_result.original_unit_price == Decimal("100.00")
    assert short_result.final_unit_price == Decimal("100.00")
    assert short_result.original_total == Decimal("100.00")
    assert short_result.final_total == Decimal("100.00")
    assert short_result.discount_amount == Decimal("0.00")

    # ---------------------------------------------------------
    # Sale totals
    # ---------------------------------------------------------

    assert result.subtotal == Decimal("150.00")
    assert result.discount_amount == Decimal("5.00")
    assert result.total == Decimal("145.00")