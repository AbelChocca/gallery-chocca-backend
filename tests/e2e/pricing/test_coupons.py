import pytest

from httpx import AsyncClient

pytestmark = pytest.mark.asyncio(
    loop_scope="session",
)

async def test_get_promotion_coupons_e2e(
    admin_client: AsyncClient,
    pricing_promotions,
    pricing_coupon,
):
    promotion = pricing_promotions[
        "promotions"
    ][0]

    response = await admin_client.get(
        f"/pricing/promotions/{promotion.id}/coupons"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

    coupon = data[0]

    assert coupon["id"] == pricing_coupon.id
    assert coupon["promotion_id"] == promotion.id
    assert coupon["code"] == "TEST20"
    assert coupon["is_active"] is True
    assert coupon["max_redemptions"] == 100
    assert coupon["max_redemptions_per_customer"] == 2
    assert coupon["used_count"] == 0

async def test_update_coupon_e2e(
    admin_client: AsyncClient,
    pricing_promotions,
    pricing_coupon,
):
    response = await admin_client.patch(
        f"/pricing/coupons/{pricing_coupon.id}",
        json={
            "code": "nuevo25",
            "max_redemptions": 250,
            "max_redemptions_per_customer": 5,
        },
    )

    assert response.status_code == 204
    assert response.content == b""

    promotion_id = pricing_coupon.promotion_id

    get_response = await admin_client.get(
        f"/pricing/promotions/{promotion_id}/coupons"
    )

    assert get_response.status_code == 200

    coupons = get_response.json()

    coupon = next(
        coupon
        for coupon in coupons
        if coupon["id"] == pricing_coupon.id
    )

    assert coupon["code"] == "NUEVO25"
    assert coupon["max_redemptions"] == 250
    assert (
        coupon["max_redemptions_per_customer"]
        == 5
    )

    assert coupon["promotion_id"] == promotion_id
    assert coupon["used_count"] == 0
    assert coupon["is_active"] is True

async def test_toggle_coupon_status_deactivates_e2e(
    admin_client: AsyncClient,
    pricing_coupon,
):
    assert pricing_coupon.is_active is True

    response = await admin_client.post(
        f"/pricing/coupons/{pricing_coupon.id}/toggle_status"
    )

    assert response.status_code == 204

    get_response = await admin_client.get(
        f"/pricing/promotions/{pricing_coupon.promotion_id}/coupons"
    )

    assert get_response.status_code == 200

    coupon = get_response.json()[0]

    assert coupon["is_active"] is False

async def test_toggle_coupon_status_twice_reactivates_e2e(
    admin_client: AsyncClient,
    pricing_coupon,
):
    first = await admin_client.post(
        f"/pricing/coupons/{pricing_coupon.id}/toggle_status"
    )

    assert first.status_code == 204

    second = await admin_client.post(
        f"/pricing/coupons/{pricing_coupon.id}/toggle_status"
    )

    assert second.status_code == 204

    get_response = await admin_client.get(
        f"/pricing/promotions/{pricing_coupon.promotion_id}/coupons"
    )

    coupon = get_response.json()[0]

    assert coupon["is_active"] is True

async def test_toggle_coupon_not_found_e2e(
    admin_client: AsyncClient,
):
    response = await admin_client.post(
        "/pricing/coupons/999999/toggle_status"
    )

    assert response.status_code == 404

async def test_create_coupon_e2e(
    admin_client: AsyncClient,
    pricing_promotions,
):
    promotion = pricing_promotions[
        "promotions"
    ][0]

    response = await admin_client.post(
        "/pricing/coupons",
        json={
            "promotion_id": promotion.id,
            "code": "verano20",
            "is_active": True,
            "max_redemptions": 100,
            "max_redemptions_per_customer": 2,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["promotion_id"] == promotion.id
    assert data["code"] == "VERANO20"
    assert data["is_active"] is True
    assert data["max_redemptions"] == 100
    assert (
        data["max_redemptions_per_customer"]
        == 2
    )
    assert data["used_count"] == 0

async def test_create_coupon_is_assigned_to_promotion_e2e(
    admin_client: AsyncClient,
    pricing_promotions,
):
    promotion = pricing_promotions[
        "promotions"
    ][0]

    create_response = await admin_client.post(
        "/pricing/coupons",
        json={
            "promotion_id": promotion.id,
            "code": "promo10",
        },
    )

    assert create_response.status_code == 201

    created = create_response.json()

    get_response = await admin_client.get(
        f"/pricing/promotions/{promotion.id}/coupons"
    )

    assert get_response.status_code == 200

    coupons = get_response.json()

    assert any(
        coupon["id"] == created["id"]
        for coupon in coupons
    )

async def test_create_coupon_rejects_missing_promotion_e2e(
    admin_client: AsyncClient,
):
    response = await admin_client.post(
        "/pricing/coupons",
        json={
            "promotion_id": 999999,
            "code": "INVALID",
        },
    )

    assert response.status_code == 404

async def test_delete_coupon_e2e(
    admin_client: AsyncClient,
    pricing_coupon,
):
    response = await admin_client.delete(
        f"/pricing/coupons/{pricing_coupon.id}"
    )

    assert response.status_code == 204
    assert response.content == b""

    get_response = await admin_client.get(
        f"/pricing/promotions/{pricing_coupon.promotion_id}/coupons"
    )

    assert get_response.status_code == 200

    coupons = get_response.json()

    assert all(
        coupon["id"] != pricing_coupon.id
        for coupon in coupons
    )

async def test_delete_coupon_not_found_e2e(
    admin_client: AsyncClient,
):
    response = await admin_client.delete(
        "/pricing/coupons/999999"
    )

    assert response.status_code == 404

async def test_get_coupon_detail_e2e(
    admin_client: AsyncClient,
    pricing_coupon,
):
    response = await admin_client.get(
        f"/pricing/coupons/{pricing_coupon.id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == pricing_coupon.id
    assert (
        data["promotion_id"]
        == pricing_coupon.promotion_id
    )

    assert data["code"] == "TEST20"
    assert data["is_active"] is True

    assert data["used_count"] == 0

    promotion = data["promotion"]

    assert (
        promotion["id"]
        == pricing_coupon.promotion_id
    )

    assert promotion["name"] is not None

async def test_get_coupon_detail_not_found_e2e(
    admin_client: AsyncClient,
):
    response = await admin_client.get(
        "/pricing/coupons/999999"
    )

    assert response.status_code == 404

async def test_get_coupon_redemptions_e2e(
    admin_client: AsyncClient,
    pricing_coupon,
    pricing_customer,
    coupon_redemptions,
):
    response = await admin_client.get(
        f"/pricing/coupons/{pricing_coupon.id}/redemptions",
        params={
            "page": 1,
            "limit": 3,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_items"] == 5
    assert data["pagination"]["current_page"] == 1
    assert data["pagination"]["total_pages"] == 2

    assert len(data["items"]) == 3

    for item in data["items"]:
        assert item["coupon_id"] == pricing_coupon.id
        assert item["customer_id"] == pricing_customer.id
        assert item["created_at"] is not None

async def test_get_coupon_redemptions_second_page_e2e(
    admin_client: AsyncClient,
    pricing_coupon,
    coupon_redemptions,
):
    response = await admin_client.get(
        f"/pricing/coupons/{pricing_coupon.id}/redemptions",
        params={
            "page": 2,
            "limit": 3,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_items"] == 5
    assert data["pagination"]["current_page"] == 2
    assert data["pagination"]["total_pages"] == 2

    assert len(data["items"]) == 2

    