import pytest_asyncio

from app.features.pricing.models.coupon import (
    CouponTable,
)
from app.features.pricing.models.coupon_redemption import (
    CouponRedemptionTable,
)


@pytest_asyncio.fixture(
    scope="function",
    loop_scope="session",
)
async def pricing_coupon(
    db_session,
    pricing_promotions,
):
    promotion = pricing_promotions[
        "promotions"
    ][0]

    coupon = CouponTable(
        promotion_id=promotion.id,
        code="TEST20",
        is_active=True,
        starts_at=None,
        ends_at=None,
        max_redemptions=100,
        max_redemptions_per_customer=2,
        used_count=0,
    )

    db_session.add(coupon)

    await db_session.commit()
    await db_session.refresh(coupon)

    return coupon

@pytest_asyncio.fixture(
    scope="function",
    loop_scope="session",
)
async def coupon_redemptions(
    db_session,
    pricing_coupon,
    pricing_customer,
):
    redemptions = [
        CouponRedemptionTable(
            coupon_id=pricing_coupon.id,
            customer_id=pricing_customer.id,
        )
        for _ in range(5)
    ]

    db_session.add_all(redemptions)

    await db_session.commit()

    for redemption in redemptions:
        await db_session.refresh(redemption)

    return redemptions