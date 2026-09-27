from datetime import datetime, timezone
from decimal import Decimal

import pytest

from app.features.sales.types.sale import SaleChannel
from app.features.products.types import CategoryType
from tests.helpers.create_test_promotion import create_category_target_promotion
from app.features.pricing.dtos.cart_pricing_dto import CartPricingContext, CartPricingItemDTO


pytestmark = pytest.mark.asyncio(
    loop_scope="session",
)

async def test_cart_pricing_applies_promotion_only_to_target_products(
    db_session,
    cart_pricing_service,
    pricing_products,
    catalog_short_product,
):
    pant = pricing_products["products"][0]
    pant_size = pricing_products["variant_sizes"][0]

    short = catalog_short_product["product"]
    short_size = catalog_short_product["variant_size"]

    await create_category_target_promotion(
        db_session,
        category=CategoryType.PANT,
        discount="10",
    )

    context = CartPricingContext(
        items=[
            CartPricingItemDTO(
            item_id=pant_size.id,
            product_id=pant.id,
            category=pant.category,
            brand=pant.brand,
            quantity=2,
            unit_price=pant.base_price,
        ),
        CartPricingItemDTO(
            item_id=short_size.id,
            product_id=short.id,
            category=short.category,
            brand=short.brand,
            quantity=1,
            unit_price=short.base_price,
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

    pant_result = next(
        item for item in result.items
        if item.product_id == pant.id
    )

    short_result = next(
        item for item in result.items
        if item.product_id == short.id
    )

    assert pant_result.original_total == Decimal("100.00")
    assert pant_result.final_total == Decimal("90.00")
    assert pant_result.discount_amount == Decimal("10.00")

    assert short_result.original_total == Decimal("80.00")
    assert short_result.final_total == Decimal("80.00")
    assert short_result.discount_amount == Decimal("0.00")

    assert result.subtotal == Decimal("180.00")
    assert result.discount_amount == Decimal("10.00")
    assert result.total == Decimal("170.00")