import pytest

from httpx import AsyncClient

pytestmark = pytest.mark.asyncio(
    loop_scope="session",
)


async def test_replace_promotion_audiences_e2e(
    admin_client: AsyncClient,
    pricing_promotions,
):
    promotion = pricing_promotions[
        "promotions"
    ][1]

    response = await admin_client.put(
        f"/pricing/promotions/{promotion.id}/audiences",
        json={
            "audiences": [
                {
                    "audience_type": "ALL_CUSTOMERS",
                    "reference_id": None,
                    "reference_value": None,
                }
            ]
        },
    )

    assert response.status_code == 204
    assert response.content == b""

    get_response = await admin_client.get(
        f"/pricing/promotions/{promotion.id}",
    )

    assert get_response.status_code == 200

    data = get_response.json()

    assert len(data["audiences"]) == 1

    audience = data["audiences"][0]

    assert (
        audience["audience_type"]
        == "ALL_CUSTOMERS"
    )

    assert audience["reference_id"] is None
    assert audience["reference_value"] is None

    assert len(data["pricing_rules"]) == 1
    assert len(data["targets"]) == 1
    assert len(data["conditions"]) == 1

async def test_replace_promotion_audiences_with_empty_list_e2e(
    admin_client: AsyncClient,
    pricing_promotions,
):
    promotion = pricing_promotions[
        "promotions"
    ][1]

    response = await admin_client.put(
        f"/pricing/promotions/{promotion.id}/audiences",
        json={
            "audiences": [],
        },
    )

    assert response.status_code == 204

    get_response = await admin_client.get(
        f"/pricing/promotions/{promotion.id}",
    )

    assert get_response.status_code == 200

    data = get_response.json()

    assert data["audiences"] == []

    assert len(data["pricing_rules"]) == 1
    assert len(data["targets"]) == 1
    assert len(data["conditions"]) == 1


async def test_replace_promotion_conditions_e2e(
    admin_client: AsyncClient,
    pricing_promotions,
):
    promotion = pricing_promotions[
        "promotions"
    ][1]

    response = await admin_client.put(
        f"/pricing/promotions/{promotion.id}/conditions",
        json={
            "conditions": [
                {
                    "condition_type": "MINIMUM_ORDER_AMOUNT",
                    "parameters": {
                        "minimum_amount": "250.00",
                    },
                    "description": (
                        "Compra mínima de S/250"
                    ),
                }
            ]
        },
    )

    assert response.status_code == 204
    assert response.content == b""

    get_response = await admin_client.get(
        f"/pricing/promotions/{promotion.id}",
    )

    assert get_response.status_code == 200

    data = get_response.json()

    assert len(data["conditions"]) == 1

    condition = data["conditions"][0]

    assert (
        condition["condition_type"]
        == "MINIMUM_ORDER_AMOUNT"
    )

    assert (
        condition["parameters"]["minimum_amount"]
        == "250.00"
    )

    assert (
        condition["description"]
        == "Compra mínima de S/250"
    )

    assert len(data["pricing_rules"]) == 1
    assert len(data["targets"]) == 1
    assert len(data["audiences"]) == 1

async def test_replace_promotion_with_multiple_conditions_e2e(
    admin_client: AsyncClient,
    pricing_promotions,
):
    promotion = pricing_promotions[
        "promotions"
    ][1]

    response = await admin_client.put(
        f"/pricing/promotions/{promotion.id}/conditions",
        json={
            "conditions": [
                {
                    "condition_type": "MINIMUM_ORDER_AMOUNT",
                    "parameters": {
                        "minimum_amount": "200.00",
                    },
                    "description": "Compra mínima",
                },
                {
                    "condition_type": "MINIMUM_PRODUCT_QUANTITY",
                    "parameters": {
                        "minimum_quantity": 3,
                    },
                    "description": "Mínimo 3 productos",
                },
            ]
        },
    )

    assert response.status_code == 204

    get_response = await admin_client.get(
        f"/pricing/promotions/{promotion.id}",
    )

    assert get_response.status_code == 200

    conditions = get_response.json()[
        "conditions"
    ]

    assert len(conditions) == 2

    condition_types = {
        condition["condition_type"]
        for condition in conditions
    }

    assert condition_types == {
        "MINIMUM_ORDER_AMOUNT",
        "MINIMUM_PRODUCT_QUANTITY",
    }

async def test_replace_promotion_targets_e2e(
    admin_client: AsyncClient,
    pricing_promotions,
):
    promotion = pricing_promotions[
        "promotions"
    ][1]

    response = await admin_client.put(
        f"/pricing/promotions/{promotion.id}/targets",
        json={
            "targets": [
                {
                    "target_type": "CATEGORY",
                    "reference_id": None,
                    "reference_value": "PANT",
                }
            ]
        },
    )

    assert response.status_code == 204
    assert response.content == b""

    get_response = await admin_client.get(
        f"/pricing/promotions/{promotion.id}",
    )

    assert get_response.status_code == 200

    data = get_response.json()

    assert len(data["targets"]) == 1

    target = data["targets"][0]

    assert target["target_type"] == "CATEGORY"
    assert target["reference_id"] is None
    assert target["reference_value"] == "PANT"

    # Otros agregados intactos
    assert len(data["pricing_rules"]) == 1
    assert len(data["audiences"]) == 1
    assert len(data["conditions"]) == 1

async def test_replace_promotion_targets_with_empty_list_e2e(
    admin_client: AsyncClient,
    pricing_promotions,
):
    promotion = pricing_promotions[
        "promotions"
    ][1]

    response = await admin_client.put(
        f"/pricing/promotions/{promotion.id}/targets",
        json={
            "targets": [],
        },
    )

    assert response.status_code == 204

    get_response = await admin_client.get(
        f"/pricing/promotions/{promotion.id}",
    )

    assert get_response.status_code == 200

    data = get_response.json()

    assert data["targets"] == []

    assert len(data["pricing_rules"]) == 1
    assert len(data["audiences"]) == 1
    assert len(data["conditions"]) == 1

async def test_replace_promotion_pricing_rules_e2e(
    admin_client: AsyncClient,
    pricing_promotions,
):
    promotion = pricing_promotions[
        "promotions"
    ][0]

    fixed_amount_rule = pricing_promotions[
        "fixed_amount_rule"
    ]

    response = await admin_client.put(
        f"/pricing/promotions/{promotion.id}/pricing-rules",
        json={
            "pricing_rules": [
                {
                    "pricing_rule_id": fixed_amount_rule.id,
                    "execution_order": 0,
                }
            ]
        },
    )

    assert response.status_code == 204
    assert response.content == b""

    get_response = await admin_client.get(
        f"/pricing/promotions/{promotion.id}",
    )

    assert get_response.status_code == 200

    data = get_response.json()

    assert len(data["pricing_rules"]) == 1

    pricing_rule = data["pricing_rules"][0]

    assert pricing_rule["id"] == fixed_amount_rule.id
    assert (
        pricing_rule["name"]
        == "Pricing Test - Fixed 20"
    )
    assert pricing_rule["type"] == "FIXED_AMOUNT"
    assert (
        pricing_rule["parameters"]["amount"]
        == "20.00"
    )

    assert len(data["audiences"]) == 1
    assert len(data["targets"]) == 1
    assert len(data["conditions"]) == 0

async def test_replace_promotion_pricing_rules_rejects_missing_rule_e2e(
    admin_client: AsyncClient,
    pricing_promotions,
):
    promotion = pricing_promotions[
        "promotions"
    ][0]

    response = await admin_client.put(
        f"/pricing/promotions/{promotion.id}/pricing-rules",
        json={
            "pricing_rules": [
                {
                    "pricing_rule_id": 999999,
                    "execution_order": 0,
                }
            ]
        },
    )

    assert response.status_code == 404

async def test_replace_promotion_with_multiple_pricing_rules_e2e(
    admin_client: AsyncClient,
    pricing_promotions,
):
    promotion = pricing_promotions[
        "promotions"
    ][0]

    percentage_rule = pricing_promotions[
        "percentage_rule"
    ]

    fixed_rule = pricing_promotions[
        "fixed_amount_rule"
    ]

    response = await admin_client.put(
        f"/pricing/promotions/{promotion.id}/pricing-rules",
        json={
            "pricing_rules": [
                {
                    "pricing_rule_id": fixed_rule.id,
                    "execution_order": 1,
                },
                {
                    "pricing_rule_id": percentage_rule.id,
                    "execution_order": 0,
                },
            ]
        },
    )

    assert response.status_code == 204

    get_response = await admin_client.get(
        f"/pricing/promotions/{promotion.id}",
    )

    assert get_response.status_code == 200

    rules = get_response.json()[
        "pricing_rules"
    ]

    assert len(rules) == 2

    assert rules[0]["id"] == percentage_rule.id
    assert rules[1]["id"] == fixed_rule.id