
from datetime import datetime, timedelta, timezone

import pytest

from httpx import AsyncClient

from app.features.complaints.types.complaint import (
    ComplaintStatus,
    ComplaintType,
)


pytestmark = pytest.mark.asyncio(
    loop_scope="session",
)


async def test_get_admin_complaints_success_e2e(
    admin_client: AsyncClient,
    complaint,
):
    response = await admin_client.get(
        "/complaints/admin",
        params={"page": 1, "limit": 100},
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert isinstance(data["items"], list)
    assert data["total_items"] >= 1
    assert data["pagination"]["current_page"] == 1
    assert data["pagination"]["total_pages"] >= 1

    item = next(
        (
            item
            for item in data["items"]
            if item["id"] == complaint.id
        ),
        None,
    )

    assert item is not None
    assert item["complaint_number"] == complaint.complaint_number
    assert item["status"] == ComplaintStatus.SUBMITTED.value
    assert item["complaint_type"] == ComplaintType.RECLAMO.value

    assert item["customer_name"] == (
        f"{complaint.first_name} {complaint.last_name}"
    )


async def test_get_admin_complaints_pagination_e2e(
    admin_client: AsyncClient,
    complaint,
    another_complaint,
):
    response = await admin_client.get(
        "/complaints/admin",
        params={"page": 1, "limit": 1},
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert len(data["items"]) == 1
    assert data["pagination"]["current_page"] == 1
    assert data["total_items"] >= 2

    expected_pages = data["total_items"]

    assert data["pagination"]["total_pages"] == expected_pages

    second_response = await admin_client.get(
        "/complaints/admin",
        params={"page": 2, "limit": 1},
    )

    assert second_response.status_code == 200

    second_data = second_response.json()

    assert len(second_data["items"]) == 1

    assert (
        second_data["items"][0]["id"]
        != data["items"][0]["id"]
    )


async def test_get_admin_complaints_filter_status_e2e(
    admin_client: AsyncClient,
    complaint_responded,
):
    response = await admin_client.get(
        "/complaints/admin",
        params={
            "status": ComplaintStatus.RESPONDED.value,
            "page": 1,
            "limit": 100,
        },
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["total_items"] >= 1

    assert all(
        item["status"] == ComplaintStatus.RESPONDED.value
        for item in data["items"]
    )

    assert any(
        item["id"] == complaint_responded.id
        for item in data["items"]
    )


async def test_get_admin_complaints_filter_type_e2e(
    admin_client: AsyncClient,
    another_complaint,
):
    response = await admin_client.get(
        "/complaints/admin",
        params={
            "complaint_type": ComplaintType.QUEJA.value,
            "page": 1,
            "limit": 100,
        },
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert all(
        item["complaint_type"] == ComplaintType.QUEJA.value
        for item in data["items"]
    )

    assert any(
        item["id"] == another_complaint.id
        for item in data["items"]
    )


async def test_get_admin_complaints_search_number_e2e(
    admin_client: AsyncClient,
    complaint,
):
    response = await admin_client.get(
        "/complaints/admin",
        params={
            "search": complaint.complaint_number,
            "page": 1,
            "limit": 20,
        },
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert any(
        item["id"] == complaint.id
        for item in data["items"]
    )


async def test_get_admin_complaints_search_customer_e2e(
    admin_client: AsyncClient,
    complaint,
):
    response = await admin_client.get(
        "/complaints/admin",
        params={
            "search": complaint.last_name,
            "page": 1,
            "limit": 20,
        },
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert any(
        item["id"] == complaint.id
        for item in data["items"]
    )


async def test_get_admin_complaints_date_filter_e2e(
    admin_client: AsyncClient,
    complaint,
):
    today = datetime.now(timezone.utc).date()

    start = today - timedelta(days=1)
    end = today + timedelta(days=1)

    response = await admin_client.get(
        "/complaints/admin",
        params={
            "created_at_from": start.isoformat(),
            "created_at_to": end.isoformat(),
            "page": 1,
            "limit": 100,
        },
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert any(
        item["id"] == complaint.id
        for item in data["items"]
    )


async def test_get_admin_complaints_order_desc_e2e(
    admin_client: AsyncClient,
    complaint,
    another_complaint,
):
    response = await admin_client.get(
        "/complaints/admin",
        params={"page": 1, "limit": 100},
    )

    assert response.status_code == 200, response.text

    items = response.json()["items"]

    ordering = [
        (
            datetime.fromisoformat(
                item["created_at"].replace("Z", "+00:00")
            ),
            item["id"],
        )
        for item in items
    ]

    assert ordering == sorted(
        ordering,
        reverse=True,
    )


@pytest.mark.parametrize(
    "params",
    [
        {"page": 0},
        {"page": -1},
        {"limit": 0},
        {"limit": 101},
        {"status": "INVALID_STATUS"},
        {"complaint_type": "INVALID_TYPE"},
    ],
)
async def test_get_admin_complaints_invalid_filters_e2e(
    admin_client: AsyncClient,
    params,
):
    response = await admin_client.get(
        "/complaints/admin",
        params=params,
    )

    assert response.status_code == 422, response.text


async def test_get_admin_complaints_requires_auth_e2e(
    http_client: AsyncClient,
):
    http_client.cookies.clear()

    response = await http_client.get(
        "/complaints/admin",
    )

    assert response.status_code in (401, 403)
