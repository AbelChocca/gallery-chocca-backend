import pytest

from httpx import AsyncClient
from sqlalchemy import select

from app.features.locations.models.locations import LocationTable
from app.features.locations.types import LocationType


pytestmark = pytest.mark.asyncio(
    loop_scope="session",
)


async def create_test_location(
    admin_client: AsyncClient,
    payload: dict,
) -> LocationTable | None:
    response = await admin_client.post(
        "/locations",
        json=payload,
    )

    assert response.status_code == 204, response.text
    assert response.content == b""

    get_response = await admin_client.get(
        "/locations/pickup",
    )

    assert get_response.status_code == 200

    return next(
        (
            location
            for location in get_response.json()
            if location["name"] == payload["name"]
        ),
        None,
    )


async def test_create_pickup_location_e2e(
    admin_client: AsyncClient,
    db_session,
    location_payload,
):
    response = await admin_client.post(
        "/locations",
        json=location_payload,
    )

    assert response.status_code == 204, response.text
    assert response.content == b""

    result = await db_session.execute(
        select(LocationTable).where(
            LocationTable.name == location_payload["name"]
        )
    )

    location = result.scalar_one_or_none()

    assert location is not None
    assert location.id is not None

    assert location.name == location_payload["name"]
    assert location.type == LocationType.STORE

    assert location.address == location_payload["address"]
    assert location.ubigeo_code == location_payload["ubigeo_code"]

    assert location.is_active is True
    assert location.pickup_enabled is True

    assert location.created_at is not None
    assert location.updated_at is not None


async def test_create_location_without_pickup_e2e(
    admin_client: AsyncClient,
    db_session,
    location_payload,
):
    payload = {
        **location_payload,
        "pickup_enabled": False,
    }

    response = await admin_client.post(
        "/locations",
        json=payload,
    )

    assert response.status_code == 204, response.text

    result = await db_session.execute(
        select(LocationTable).where(
            LocationTable.name == payload["name"]
        )
    )

    location = result.scalar_one()

    assert location.is_active is True
    assert location.pickup_enabled is False


@pytest.mark.parametrize(
    "changes",
    [
        {"type": LocationType.WAREHOUSE.value},
        {"pickup_enabled": True, "is_active": False},
        {"address": None},
        {"ubigeo_code": None},
    ],
)
async def test_create_invalid_pickup_location_e2e(
    admin_client: AsyncClient,
    db_session,
    location_payload,
    changes,
):
    payload = {
        **location_payload,
        **changes,
    }

    response = await admin_client.post(
        "/locations",
        json=payload,
    )

    assert response.status_code in (400, 422), response.text

    result = await db_session.execute(
        select(LocationTable).where(
            LocationTable.name == payload["name"]
        )
    )

    assert result.scalar_one_or_none() is None


async def test_create_location_invalid_ubigeo_e2e(
    admin_client: AsyncClient,
    location_payload,
):
    payload = {
        **location_payload,
        "ubigeo_code": "ABC123",
    }

    response = await admin_client.post(
        "/locations",
        json=payload,
    )

    assert response.status_code == 422


# ============================================================
# GET /locations/pickup
# ============================================================

async def test_get_pickup_locations_public_e2e(
    admin_client: AsyncClient,
    location_payload,
):
    created = await create_test_location(
        admin_client=admin_client,
        payload=location_payload,
    )

    assert created is not None

    response = await admin_client.get(
        "/locations/pickup"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    location = next(
        item
        for item in data
        if item["id"] == created["id"]
    )

    assert location["name"] == location_payload["name"]
    assert location["address"] == location_payload["address"]
    assert location["ubigeo_code"] == location_payload["ubigeo_code"]

    assert location["phone"] == location_payload["phone"]
    assert location["reference"] == location_payload["reference"]

    # No debe exponer propiedades administrativas.
    assert "external_provider" not in location
    assert "external_code" not in location
    assert "pickup_enabled" not in location


async def test_get_pickup_locations_without_auth_e2e(
    http_client: AsyncClient,
):
    http_client.cookies.clear()

    response = await http_client.get(
        "/locations/pickup",
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_pickup_disabled_location_not_listed_e2e(
    admin_client: AsyncClient,
    location_payload,
):
    payload = {
        **location_payload,
        "pickup_enabled": False,
    }

    response = await admin_client.post(
        "/locations",
        json=payload,
    )

    assert response.status_code == 204

    get_response = await admin_client.get(
        "/locations/pickup",
    )

    assert get_response.status_code == 200

    names = {
        item["name"]
        for item in get_response.json()
    }

    assert payload["name"] not in names


# ============================================================
# DELETE /locations/{location_id}
# ============================================================

async def test_delete_location_soft_delete_e2e(
    admin_client: AsyncClient,
    db_session,
    location_payload,
):
    created = await create_test_location(
        admin_client=admin_client,
        payload=location_payload,
    )

    assert created is not None

    location_id = created["id"]

    response = await admin_client.delete(
        f"/locations/{location_id}"
    )

    assert response.status_code == 204, response.text
    assert response.content == b""

    # Verificamos persistencia real en PostgreSQL.
    db_session.expire_all()

    result = await db_session.execute(
        select(LocationTable).where(
            LocationTable.id == location_id
        )
    )

    location = result.scalar_one_or_none()

    # Baja lógica, no DELETE físico.
    assert location is not None
    assert location.is_active is False
    assert location.pickup_enabled is False

    # Tampoco debe estar disponible para nuevos recojos.
    get_response = await admin_client.get(
        "/locations/pickup",
    )

    assert get_response.status_code == 200

    ids = {
        item["id"]
        for item in get_response.json()
    }

    assert location_id not in ids


async def test_delete_location_not_found_e2e(
    admin_client: AsyncClient,
):
    response = await admin_client.delete(
        "/locations/999999999"
    )

    assert response.status_code == 404


async def test_delete_location_invalid_id_e2e(
    admin_client: AsyncClient,
):
    response = await admin_client.delete(
        "/locations/0"
    )

    assert response.status_code == 422


# ============================================================
# AUTHORIZATION
# ============================================================

async def test_create_location_requires_auth_e2e(
    http_client: AsyncClient,
    location_payload,
):
    http_client.cookies.clear()

    response = await http_client.post(
        "/locations",
        json=location_payload,
    )

    assert response.status_code in (401, 403)


async def test_delete_location_requires_auth_e2e(
    http_client: AsyncClient,
):
    http_client.cookies.clear()

    response = await http_client.delete(
        "/locations/999999999"
    )

    assert response.status_code in (401, 403)
