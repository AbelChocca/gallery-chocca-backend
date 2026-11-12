from datetime import datetime
from uuid import UUID

import pytest

from httpx import AsyncClient
from sqlalchemy import select

from app.features.complaints.models.complaint import ComplaintTable
from app.features.complaints.types.complaint import (
    ComplaintStatus,
    ComplaintType,
    ComplaintResponseChannel,
)


pytestmark = pytest.mark.asyncio(
    loop_scope="session",
)


async def test_create_complaint_success_e2e(
    http_client: AsyncClient,
    db_session,
    complaint_payload,
    fake_mail_service,
):
    http_client.cookies.clear()

    response = await http_client.post(
        "/complaints",
        json=complaint_payload,
    )

    assert response.status_code == 201, response.text

    data = response.json()

    assert UUID(data["public_id"])
    assert data["complaint_number"].startswith("LR-")
    assert data["status"] == ComplaintStatus.SUBMITTED.value
    assert datetime.fromisoformat(
        data["created_at"].replace("Z", "+00:00")
    )

    result = await db_session.execute(
        select(ComplaintTable).where(
            ComplaintTable.complaint_number
            == data["complaint_number"]
        )
    )

    complaint = result.scalar_one_or_none()

    assert complaint is not None
    assert complaint.public_id == UUID(data["public_id"])

    assert complaint.first_name == complaint_payload["first_name"]
    assert complaint.last_name == complaint_payload["last_name"]
    assert complaint.email == complaint_payload["email"]
    assert complaint.status == ComplaintStatus.SUBMITTED

    assert complaint.response_channel == ComplaintResponseChannel.EMAIL
    assert complaint.response_due_at is not None

    assert len(fake_mail_service.sent) == 1
    assert fake_mail_service.sent[0].to == complaint_payload["email"]


async def test_create_queja_success_e2e(
    http_client: AsyncClient,
    db_session,
    complaint_payload,
):
    http_client.cookies.clear()

    payload = {
        **complaint_payload,
        "complaint_type": ComplaintType.QUEJA.value,
    }

    response = await http_client.post(
        "/complaints",
        json=payload,
    )

    assert response.status_code == 201, response.text

    data = response.json()

    result = await db_session.execute(
        select(ComplaintTable).where(
            ComplaintTable.complaint_number
            == data["complaint_number"]
        )
    )

    complaint = result.scalar_one()

    assert complaint.complaint_type == ComplaintType.QUEJA


async def test_create_complaint_generates_unique_numbers_e2e(
    http_client: AsyncClient,
    complaint_payload,
):
    http_client.cookies.clear()

    first = await http_client.post(
        "/complaints",
        json=complaint_payload,
    )

    second = await http_client.post(
        "/complaints",
        json=complaint_payload,
    )

    assert first.status_code == 201, first.text
    assert second.status_code == 201, second.text

    first_data = first.json()
    second_data = second.json()

    assert first_data["public_id"] != second_data["public_id"]
    assert (
        first_data["complaint_number"]
        != second_data["complaint_number"]
    )


@pytest.mark.parametrize(
    "changes",
    [
        {"first_name": ""},
        {"last_name": ""},
        {"document_number": "123"},
        {"document_number": "ABCDEFGH"},
        {"email": "correo-invalido"},
        {"detail": ""},
        {"requested_solution": ""},
    ],
)
async def test_create_complaint_invalid_data_e2e(
    http_client: AsyncClient,
    complaint_payload,
    changes,
):
    http_client.cookies.clear()

    payload = {
        **complaint_payload,
        **changes,
    }

    response = await http_client.post(
        "/complaints",
        json=payload,
    )

    assert response.status_code == 422, response.text


async def test_create_complaint_requires_email_for_email_channel_e2e(
    http_client: AsyncClient,
    complaint_payload,
):
    http_client.cookies.clear()

    payload = {
        **complaint_payload,
        "email": None,
        "response_channel": ComplaintResponseChannel.EMAIL.value,
    }

    response = await http_client.post(
        "/complaints",
        json=payload,
    )

    assert response.status_code == 422


async def test_create_complaint_carta_without_email_e2e(
    http_client: AsyncClient,
    db_session,
    complaint_payload,
    fake_mail_service,
):
    http_client.cookies.clear()

    payload = {
        **complaint_payload,
        "email": None,
        "response_channel": ComplaintResponseChannel.CARTA.value,
    }

    response = await http_client.post(
        "/complaints",
        json=payload,
    )

    assert response.status_code == 201, response.text

    data = response.json()

    result = await db_session.execute(
        select(ComplaintTable).where(
            ComplaintTable.complaint_number
            == data["complaint_number"]
        )
    )

    complaint = result.scalar_one()

    assert complaint.response_channel == ComplaintResponseChannel.CARTA
    assert complaint.email is None

    assert len(fake_mail_service.sent) == 0


async def test_create_minor_without_representative_e2e(
    http_client: AsyncClient,
    complaint_payload,
):
    http_client.cookies.clear()

    payload = {
        **complaint_payload,
        "is_minor": True,
        "representative_name": None,
        "representative_document": None,
    }

    response = await http_client.post(
        "/complaints",
        json=payload,
    )

    assert response.status_code == 422


async def test_create_minor_with_representative_e2e(
    http_client: AsyncClient,
    db_session,
    complaint_payload,
):
    http_client.cookies.clear()

    payload = {
        **complaint_payload,
        "is_minor": True,
        "representative_name": "Maria Perez",
        "representative_document": "87654321",
    }

    response = await http_client.post(
        "/complaints",
        json=payload,
    )

    assert response.status_code == 201, response.text

    number = response.json()["complaint_number"]

    result = await db_session.execute(
        select(ComplaintTable).where(
            ComplaintTable.complaint_number == number
        )
    )

    complaint = result.scalar_one()

    assert complaint.is_minor is True
    assert complaint.representative_name == "Maria Perez"
    assert complaint.representative_document == "87654321"


async def test_create_complaint_mail_failure_preserves_record_e2e(
    http_client: AsyncClient,
    db_session,
    complaint_payload,
    fake_mail_service,
):
    http_client.cookies.clear()

    fake_mail_service.fail_with = RuntimeError(
        "Simulated mail provider failure"
    )

    response = await http_client.post(
        "/complaints",
        json=complaint_payload,
    )

    # El contrato actual permite registrar la reclamación
    # aunque falle el envío de la constancia.
    assert response.status_code == 201, response.text

    data = response.json()

    assert data["receipt_email_sent"] is False

    result = await db_session.execute(
        select(ComplaintTable).where(
            ComplaintTable.complaint_number
            == data["complaint_number"]
        )
    )

    assert result.scalar_one_or_none() is not None


async def test_create_complaint_rejects_extra_fields_e2e(
    http_client: AsyncClient,
    complaint_payload,
):
    http_client.cookies.clear()

    payload = {
        **complaint_payload,
        "status": "RESPONDED",
        "provider_ruc": "99999999999",
    }

    response = await http_client.post(
        "/complaints",
        json=payload,
    )

    assert response.status_code == 422
