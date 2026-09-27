import pytest
from pprint import pprint

pytestmark = pytest.mark.asyncio(
    loop_scope="session"
)

from httpx import AsyncClient

from decimal import Decimal

from tests.helpers.create_order_subtotal_promotion import (
    create_wholesale_bgoo_order_promotion,
)
from app.features.sales.types.customer import CustomerType

async def test_toggle_promotion_status_deactivates_e2e(
    admin_client: AsyncClient,
    pricing_promotions,
):
    promotion = pricing_promotions[
        "promotions"
    ][0]

    assert promotion.is_active is True

    response = await admin_client.post(
        f"/pricing/promotions/{promotion.id}/toggle_status"
    )

    assert response.status_code == 204
    assert response.content == b""

    get_response = await admin_client.get(
        f"/pricing/promotions/{promotion.id}"
    )

    assert get_response.status_code == 200

    data = get_response.json()

    assert data["is_active"] is False

async def test_toggle_promotion_status_activates_e2e(
    admin_client: AsyncClient,
    pricing_promotions,
):
    promotion = pricing_promotions[
        "promotions"
    ][0]

    first_response = await admin_client.post(
        f"/pricing/promotions/{promotion.id}/toggle_status"
    )

    assert first_response.status_code == 204

    second_response = await admin_client.post(
        f"/pricing/promotions/{promotion.id}/toggle_status"
    )

    assert second_response.status_code == 204

    get_response = await admin_client.get(
        f"/pricing/promotions/{promotion.id}"
    )

    assert get_response.status_code == 200

    data = get_response.json()

    assert data["is_active"] is True

async def test_toggle_promotion_status_not_found_e2e(
    admin_client: AsyncClient,
):
    response = await admin_client.post(
        "/pricing/promotions/999999/toggle_status"
    )

    assert response.status_code == 404

async def test_wholesale_bgoo_order_subtotal_promotion_e2e(
    admin_client: AsyncClient,
    db_session,
    product,
    variant,
    variant_size,
    location,
    variant_size_inventory,
    wholesale_pricing_customer,
    wholesale_cart,
):
    await create_wholesale_bgoo_order_promotion(
        db_session,
    )

    assert wholesale_pricing_customer.user_id is not None
    assert wholesale_pricing_customer.customer_type == CustomerType.WHOLESALE

    response = await admin_client.get(
        "/cart"
    )

    assert response.status_code == 200

    data = response.json()

    pprint(data)

    assert data is not None

    assert Decimal(data["subtotal"]) == Decimal("600.00")
    assert Decimal(data["discount_amount"]) == Decimal("90.00")
    assert Decimal(data["total"]) == Decimal("510.00")

    assert data["total_items"] == 2

    assert len(data["items"]) == 1

    item = data["items"][0]

    assert item["product_id"] == product.id
    assert item["variant_id"] == variant.id
    assert item["variant_size_id"] == variant_size.id

    assert item["quantity"] == 2

    assert Decimal(item["original_price"]) == Decimal("300.00")
    assert Decimal(item["final_price"]) == Decimal("300.00")

    assert Decimal(item["original_total"]) == Decimal("600.00")
    assert Decimal(item["final_total"]) == Decimal("600.00")

    # ORDER_SUBTOTAL no modifica directamente la línea
    assert Decimal(item["discount_amount"]) == Decimal("0.00")
    assert item["has_discount"] is False

    # El descuento vive en el carrito
    assert len(data["applied_promotions"]) == 1

    applied = data["applied_promotions"][0]

    assert applied["name"] == "Mayoristas BGOO - 15%"
    assert Decimal(applied["discount_amount"]) == Decimal("90.00")