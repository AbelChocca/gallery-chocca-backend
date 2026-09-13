from datetime import datetime, timezone, timedelta
from decimal import Decimal

import pytest

from app.features.pricing.dtos.sale_pricing import (
    PricingItemDTO,
    SalePricingContext,
)
from app.features.sales.types.sale import SaleChannel
from app.core.exceptions import ValidationError
from app.features.pricing.models.coupon import CouponTable
from app.features.pricing.models.coupon_redemption import CouponRedemptionTable

@pytest.mark.asyncio
async def test_calculate_rejects_inactive_coupon(
    db_session,
    sale_pricing_service,
    pricing_products,
    pricing_promotions,
    pricing_customer,
):
    products = pricing_products["products"]
    customer = pricing_customer

    coupon = CouponTable(
        promotion_id=pricing_promotions["promotions"][0].id,
        code="INACTIVE-COUPON",
        is_active=False,
        max_redemptions=100,
        max_redemptions_per_customer=1,
        used_count=0,
    )

    db_session.add(coupon)
    await db_session.commit()

    now = datetime.now(timezone.utc)

    context = SalePricingContext(
        items=[
            PricingItemDTO(
                product_id=products[0].id,
                quantity=2,
                category=products[0].category,
                brand=products[0].brand,
                unit_price=Decimal("50.00"),
            )
        ],
        sale_channel=SaleChannel.ECOMMERCE,
        now=now,
        customer_id=customer.id,
        customer_type=customer.customer_type,
        coupon_code="INACTIVE-COUPON",
        shipping_cost=Decimal("15.00"),
    )

    with pytest.raises(
        ValidationError,
        match="El cupon esta inactivo.",
    ):
        await sale_pricing_service.calculate(context=context)

@pytest.mark.asyncio
async def test_calculate_rejects_coupon_before_start_date(
    db_session,
    sale_pricing_service,
    pricing_products,
    pricing_promotions,
    pricing_customer,
):
    products = pricing_products["products"]
    customer = pricing_customer

    now = datetime.now(timezone.utc)

    coupon = CouponTable(
        promotion_id=pricing_promotions["promotions"][0].id,
        code="NOT-STARTED-COUPON",
        is_active=True,
        starts_at=now + timedelta(days=1),
        ends_at=None,
        max_redemptions=100,
        max_redemptions_per_customer=1,
        used_count=0,
    )

    db_session.add(coupon)
    await db_session.commit()

    context = SalePricingContext(
        items=[
            PricingItemDTO(
                product_id=products[0].id,
                quantity=2,
                category=products[0].category,
                brand=products[0].brand,
                unit_price=Decimal("50.00"),
            )
        ],
        sale_channel=SaleChannel.ECOMMERCE,
        now=now,
        customer_id=customer.id,
        customer_type=customer.customer_type,
        coupon_code="NOT-STARTED-COUPON",
        shipping_cost=Decimal("15.00"),
    )

    with pytest.raises(
        ValidationError,
        match="El cupon aun no esta disponible.",
    ):
        await sale_pricing_service.calculate(context=context)

@pytest.mark.asyncio
async def test_calculate_rejects_expired_coupon(
    db_session,
    sale_pricing_service,
    pricing_products,
    pricing_promotions,
    pricing_customer,
):
    products = pricing_products["products"]
    customer = pricing_customer

    now = datetime.now(timezone.utc)

    coupon = CouponTable(
        promotion_id=pricing_promotions["promotions"][0].id,
        code="EXPIRED-COUPON",
        is_active=True,
        starts_at=now - timedelta(days=2),
        ends_at=now - timedelta(days=1),
        max_redemptions=100,
        max_redemptions_per_customer=1,
        used_count=0,
    )

    db_session.add(coupon)
    await db_session.commit()

    context = SalePricingContext(
        items=[
            PricingItemDTO(
                product_id=products[0].id,
                quantity=2,
                category=products[0].category,
                brand=products[0].brand,
                unit_price=Decimal("50.00"),
            )
        ],
        sale_channel=SaleChannel.ECOMMERCE,
        now=now,
        customer_id=customer.id,
        customer_type=customer.customer_type,
        coupon_code="EXPIRED-COUPON",
        shipping_cost=Decimal("15.00"),
    )

    with pytest.raises(
        ValidationError,
        match="El cupon ha expirado.",
    ):
        await sale_pricing_service.calculate(context=context)

@pytest.mark.asyncio
async def test_calculate_rejects_exhausted_coupon(
    db_session,
    sale_pricing_service,
    pricing_products,
    pricing_promotions,
    pricing_customer,
):
    products = pricing_products["products"]
    customer = pricing_customer

    coupon = CouponTable(
        promotion_id=pricing_promotions["promotions"][0].id,
        code="EXHAUSTED-COUPON",
        is_active=True,
        starts_at=None,
        ends_at=None,
        max_redemptions=100,
        max_redemptions_per_customer=1,
        used_count=100,
    )

    db_session.add(coupon)
    await db_session.commit()

    context = SalePricingContext(
        items=[
            PricingItemDTO(
                product_id=products[0].id,
                quantity=2,
                category=products[0].category,
                brand=products[0].brand,
                unit_price=Decimal("50.00"),
            )
        ],
        sale_channel=SaleChannel.ECOMMERCE,
        now=datetime.now(timezone.utc),
        customer_id=customer.id,
        customer_type=customer.customer_type,
        coupon_code="EXHAUSTED-COUPON",
        shipping_cost=Decimal("15.00"),
    )

    with pytest.raises(
        ValidationError,
        match="El cupon alcanzo el maximo numero de canjeos.",
    ):
        await sale_pricing_service.calculate(context=context)

@pytest.mark.asyncio
async def test_calculate_rejects_customer_coupon_redemption_limit(
    db_session,
    sale_pricing_service,
    pricing_products,
    pricing_promotions,
    pricing_customer,
):
    products = pricing_products["products"]
    customer = pricing_customer

    coupon = CouponTable(
        promotion_id=pricing_promotions["promotions"][0].id,
        code="CUSTOMER-LIMIT-COUPON",
        is_active=True,
        starts_at=None,
        ends_at=None,
        max_redemptions=100,
        max_redemptions_per_customer=1,
        used_count=1,
    )

    db_session.add(coupon)
    await db_session.commit()
    await db_session.refresh(coupon)

    redemption = CouponRedemptionTable(
        coupon_id=coupon.id,
        customer_id=customer.id,
    )

    db_session.add(redemption)
    await db_session.commit()

    now = datetime.now(timezone.utc)

    context = SalePricingContext(
        items=[
            PricingItemDTO(
                product_id=products[0].id,
                quantity=2,
                category=products[0].category,
                brand=products[0].brand,
                unit_price=Decimal("50.00"),
            )
        ],
        sale_channel=SaleChannel.ECOMMERCE,
        now=now,
        customer_id=customer.id,
        customer_type=customer.customer_type,
        coupon_code="CUSTOMER-LIMIT-COUPON",
        shipping_cost=Decimal("15.00"),
    )

    with pytest.raises(
        ValidationError,
        match="El cliente alcanzo el maximo numero de canjeos del cupon.",
    ):
        await sale_pricing_service.calculate(context=context)