
from datetime import datetime
from decimal import Decimal
from uuid import UUID

import pytest

from httpx import AsyncClient

from app.features.complaints.types.complaint import (
    ComplaintStatus,
    ComplaintType,
    ComplaintGoodType,
    ComplaintResponseChannel,
)


pytestmark = pytest.mark.asyncio(
    loop_scope="session",
)


async def test_get_admin_complaint_detail_success_e2e(
    admin_client: AsyncClient,
    complaint,
):
    response = await admin_client.get(
        f"/complaints/admin/{complaint.id}"
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["id"] == complaint.id
    assert data["complaint_number"] == complaint.complaint_number
    assert UUID(data["public_id"]) == complaint.public_id

    assert data["status"] == ComplaintStatus.SUBMITTED.value
    assert data["complaint_type"] == ComplaintType.RECLAMO.value
    assert data["good_type"] == ComplaintGoodType.PRODUCTO.value

    assert (
        data["response_channel"]
        == ComplaintResponseChannel.EMAIL.value
    )


async def test_get_admin_complaint_detail_customer_data_e2e(
    admin_client: AsyncClient,
    complaint,
):
    response = await admin_client.get(
        f"/complaints/admin/{complaint.id}"
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["first_name"] == complaint.first_name
    assert data["last_name"] == complaint.last_name
    assert data["document_number"] == complaint.document_number
    assert data["email"] == complaint.email
    assert data["phone"] == complaint.phone
    assert data["address"] == complaint.address

    assert data["is_minor"] is False
    assert data["representative_name"] is None
    assert data["representative_document"] is None


async def test_get_admin_complaint_detail_product_data_e2e(
    admin_client: AsyncClient,
    complaint,
):
    response = await admin_client.get(
        f"/complaints/admin/{complaint.id}"
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["product_description"] == complaint.product_description

    assert Decimal(str(data["amount"])) == complaint.amount

    assert data["detail"] == complaint.detail
    assert data["requested_solution"] == complaint.requested_solution
    assert data["order_number"] == complaint.order_number


async def test_get_admin_complaint_detail_provider_data_e2e(
    admin_client: AsyncClient,
    complaint,
):
    response = await admin_client.get(
        f"/complaints/admin/{complaint.id}"
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert (
        data["provider_legal_name"]
        == complaint.provider_legal_name
    )

    assert data["provider_ruc"] == complaint.provider_ruc

    assert (
        data["provider_address"]
        == complaint.provider_address
    )


async def test_get_admin_complaint_detail_dates_e2e(
    admin_client: AsyncClient,
    complaint,
):
    response = await admin_client.get(
        f"/complaints/admin/{complaint.id}"
    )

    assert response.status_code == 200, response.text

    data = response.json()

    created_at = datetime.fromisoformat(
        data["created_at"].replace("Z", "+00:00")
    )

    updated_at = datetime.fromisoformat(
        data["updated_at"].replace("Z", "+00:00")
    )

    due_at = datetime.fromisoformat(
        data["response_due_at"].replace("Z", "+00:00")
    )

    assert created_at == complaint.created_at
    assert updated_at == complaint.updated_at
    assert due_at == complaint.response_due_at

    assert data["responded_at"] is None


async def test_get_admin_complaint_detail_responded_e2e(
    admin_client: AsyncClient,
    complaint_responded,
):
    response = await admin_client.get(
        f"/complaints/admin/{complaint_responded.id}"
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["status"] == ComplaintStatus.RESPONDED.value
    assert data["responded_at"] is not None


async def test_get_admin_complaint_detail_carta_e2e(
    admin_client: AsyncClient,
    complaint_carta,
):
    response = await admin_client.get(
        f"/complaints/admin/{complaint_carta.id}"
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert (
        data["response_channel"]
        == ComplaintResponseChannel.CARTA.value
    )
    assert data["email"] is None


async def test_get_admin_complaint_detail_not_found_e2e(
    admin_client: AsyncClient,
):
    response = await admin_client.get(
        "/complaints/admin/999999999"
    )

    assert response.status_code == 404


@pytest.mark.parametrize(
    "invalid_id",
    [
        "0",
        "-1",
        "abc",
    ],
)
async def test_get_admin_complaint_detail_invalid_id_e2e(
    admin_client: AsyncClient,
    invalid_id,
):
    response = await admin_client.get(
        f"/complaints/admin/{invalid_id}"
    )

    assert response.status_code == 422


async def test_get_admin_complaint_detail_requires_auth_e2e(
    http_client: AsyncClient,
    complaint,
):
    http_client.cookies.clear()

    response = await http_client.get(
        f"/complaints/admin/{complaint.id}"
    )

    assert response.status_code in (401, 403)
