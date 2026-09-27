import pytest

pytestmark = pytest.mark.asyncio(
    loop_scope="session"
)

from httpx import AsyncClient


async def test_create_promotion_e2e(
    admin_client: AsyncClient,
):
    payload = {
        "name": "Promo verano",
        "description": "Descuento de verano",
        "sales_channel": "ECOMMERCE",
        "stacking_mode": "STACKABLE",
        "application_scope": "PER_ITEM",
        "priority": 10,
        "is_active": True,
        "pricing_rules": [
            {
                "name": "Descuento 10%",
                "description": "10% de descuento",
                "type": "PERCENTAGE",
                "parameters": {
                    "percentage": "10"
                },
                "execution_order": 0,
            }
        ],
        "audiences": [
            {
                "audience_type": "ALL_CUSTOMERS",
                "reference_id": None,
                "reference_value": None,
            }
        ],
        "targets": [
            {
                "target_type": "CATEGORY",
                "reference_id": None,
                "reference_value": "PANT",
            }
        ],
        "conditions": [],
    }

    response = await admin_client.post(
        "/pricing/promotions",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Promo verano"
    assert data["priority"] == 10
    assert data["is_active"] is True

    assert len(data["pricing_rules"]) == 1
    assert len(data["audiences"]) == 1
    assert len(data["targets"]) == 1

    assert (
        data["pricing_rules"][0]["type"]
        == "PERCENTAGE"
    )

    assert (
        data["audiences"][0]["audience_type"]
        == "ALL_CUSTOMERS"
    )

    assert (
        data["targets"][0]["target_type"]
       == "CATEGORY"
    )

async def test_get_promotions_e2e(
    admin_client: AsyncClient,
    pricing_promotions,
):
    response = await admin_client.get(
        "/pricing/promotions",
        params={
            "page": 1,
            "limit": 20,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_items"] >= 2
    assert data["pagination"]["current_page"] == 1

    items = data["items"]

    assert len(items) >= 2

    promotion_1 = next(
        item
        for item in items
        if item["name"] == "Pricing Test - 10% OFF"
    )

    promotion_2 = next(
        item
        for item in items
        if item["name"] == "Pricing Test - S/20 OFF"
    )

    assert promotion_1["sales_channel"] == "ECOMMERCE"
    assert promotion_1["stacking_mode"] == "STACKABLE"
    assert promotion_1["is_active"] is True
    assert promotion_1["status"] == "ACTIVE"

    assert promotion_1["pricing_rules_count"] == 1
    assert promotion_1["targets_count"] == 1
    assert promotion_1["audiences_count"] == 1
    assert promotion_1["conditions_count"] == 0
    assert promotion_1["coupons_count"] == 0
    assert promotion_1["has_coupon"] is False

    assert promotion_2["sales_channel"] == "ECOMMERCE"
    assert promotion_2["stacking_mode"] == "EXCLUSIVE"
    assert promotion_2["is_active"] is True
    assert promotion_2["status"] == "ACTIVE"

    assert promotion_2["pricing_rules_count"] == 1
    assert promotion_2["targets_count"] == 1
    assert promotion_2["audiences_count"] == 1
    assert promotion_2["conditions_count"] == 1
    assert promotion_2["coupons_count"] == 0
    assert promotion_2["has_coupon"] is False

async def test_get_promotions_filters_by_search_e2e(
    admin_client: AsyncClient,
    pricing_promotions,
):
    response = await admin_client.get(
        "/pricing/promotions",
        params={
            "search": "mayoristas",
            "page": 1,
            "limit": 20,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_items"] == 1
    assert len(data["items"]) == 1

    promotion = data["items"][0]

    assert promotion["name"] == "Pricing Test - S/20 OFF"

async def test_get_promotions_filters_by_sales_channel_e2e(
    admin_client: AsyncClient,
    pricing_promotions,
):
    response = await admin_client.get(
        "/pricing/promotions",
        params={
            "sales_channel": "ECOMMERCE",
            "page": 1,
            "limit": 20,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_items"] >= 2

    for item in data["items"]:
        assert item["sales_channel"] == "ECOMMERCE"

async def test_get_promotion_detail_e2e(
    admin_client: AsyncClient,
    pricing_promotions,
):
    promotion = pricing_promotions["promotions"][1]

    response = await admin_client.get(
        f"/pricing/promotions/{promotion.id}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == promotion.id
    assert data["name"] == "Pricing Test - S/20 OFF"
    assert data["description"] == (
        "Promocion exclusiva para clientes mayoristas"
    )

    assert data["sales_channel"] == "ECOMMERCE"
    assert data["stacking_mode"] == "EXCLUSIVE"
    assert data["priority"] == 10
    assert data["is_active"] is True

    assert len(data["pricing_rules"]) == 1
    assert len(data["audiences"]) == 1
    assert len(data["targets"]) == 1
    assert len(data["conditions"]) == 1
    assert len(data["coupons"]) == 0

    pricing_rule = data["pricing_rules"][0]

    assert pricing_rule["name"] == "Pricing Test - Fixed 20"
    assert pricing_rule["type"] == "FIXED_AMOUNT"
    assert pricing_rule["parameters"]["amount"] == "20.00"

    audience = data["audiences"][0]

    assert (
        audience["audience_type"]
        == "CUSTOMER_GROUP"
    )
    assert (
        audience["reference_value"]
        == "WHOLESALE"
    )

    target = data["targets"][0]

    assert target["target_type"] == "PRODUCT"
    assert (
        target["reference_id"]
        == pricing_promotions["targets"][1].reference_id
    )

    condition = data["conditions"][0]

    assert (
        condition["condition_type"]
        == "PAYMENT_METHOD"
    )
    assert (
        condition["parameters"]["payment_method"]
        == "YAPE"
    )

async def test_get_promotion_detail_not_found_e2e(
    admin_client: AsyncClient,
):
    response = await admin_client.get(
        "/pricing/promotions/999999",
    )

    assert response.status_code == 404

async def test_delete_promotion_e2e(
    admin_client: AsyncClient,
    pricing_promotions,
):
    promotion = pricing_promotions[
        "promotions"
    ][0]

    response = await admin_client.delete(
        f"/pricing/promotions/{promotion.id}",
    )

    assert response.status_code == 204

    get_response = await admin_client.get(
        f"/pricing/promotions/{promotion.id}",
    )

    assert get_response.status_code == 404

async def test_delete_promotion_not_found_e2e(
    admin_client: AsyncClient,
):
    response = await admin_client.delete(
        "/pricing/promotions/999999",
    )

    assert response.status_code == 404

async def test_update_promotion_e2e(
    admin_client: AsyncClient,
    pricing_promotions,
):
    promotion = pricing_promotions[
        "promotions"
    ][1]

    response = await admin_client.patch(
        f"/pricing/promotions/{promotion.id}",
        json={
            "name": "Promo mayoristas actualizada",
            "description": "Descripción actualizada",
            "priority": 99,
            "is_active": False,
        },
    )

    assert response.status_code == 204
    assert response.content == b""

    get_response = await admin_client.get(
        f"/pricing/promotions/{promotion.id}",
    )

    assert get_response.status_code == 200

    data = get_response.json()

    assert data["id"] == promotion.id
    assert (
        data["name"]
        == "Promo mayoristas actualizada"
    )
    assert (
        data["description"]
        == "Descripción actualizada"
    )
    assert data["priority"] == 99
    assert data["is_active"] is False

    assert (
        data["sales_channel"]
        == "ECOMMERCE"
    )
    assert (
        data["stacking_mode"]
        == "EXCLUSIVE"
    )

    assert len(data["pricing_rules"]) == 1
    assert len(data["audiences"]) == 1
    assert len(data["targets"]) == 1
    assert len(data["conditions"]) == 1
    assert len(data["coupons"]) == 0

    pricing_rule = data["pricing_rules"][0]

    assert (
        pricing_rule["name"]
        == "Pricing Test - Fixed 20"
    )
    assert (
        pricing_rule["type"]
        == "FIXED_AMOUNT"
    )

    audience = data["audiences"][0]

    assert (
        audience["audience_type"]
        == "CUSTOMER_GROUP"
    )
    assert (
        audience["reference_value"]
        == "WHOLESALE"
    )

    target = data["targets"][0]

    assert target["target_type"] == "PRODUCT"

    condition = data["conditions"][0]

    assert (
        condition["condition_type"]
        == "PAYMENT_METHOD"
    )
    assert (
        condition["parameters"]["payment_method"]
        == "YAPE"
    )

async def test_update_promotion_not_found_e2e(
    admin_client: AsyncClient,
):
    response = await admin_client.patch(
        "/pricing/promotions/999999",
        json={
            "name": "No existe",
        },
    )

    assert response.status_code == 404