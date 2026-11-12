
import pytest

from httpx import AsyncClient
from sqlalchemy import select

from app.features.complaints.models.complaint import ComplaintTable
from app.features.complaints.models.complaint_response import (
    ComplaintResponseTable,
)

from app.features.complaints.types.complaint import (
    ComplaintStatus,
)
from app.features.complaints.types.complaint_response import (
    ComplaintResponseStatus,
)


pytestmark = pytest.mark.asyncio(
    loop_scope="session",
)


def send_url(
    complaint_id: int,
    response_id: int,
) -> str:
    return (
        f"/complaints/admin/{complaint_id}"
        f"/responses/{response_id}/send"
    )


async def load_saved_state(
    db_session,
    *,
    complaint_id: int,
    response_id: int,
):
    # El endpoint utiliza otra sesión / UoW.
    db_session.expire_all()

    complaint_result = await db_session.execute(
        select(ComplaintTable).where(
            ComplaintTable.id == complaint_id
        )
    )

    response_result = await db_session.execute(
        select(ComplaintResponseTable).where(
            ComplaintResponseTable.id == response_id
        )
    )

    return (
        complaint_result.scalar_one(),
        response_result.scalar_one(),
    )


# ============================================================
# SUCCESSFUL EMAIL SEND
# ============================================================

async def test_send_response_success_e2e(
    admin_client: AsyncClient,
    db_session,
    complaint,
    complaint_response_draft,
    fake_mail_service,
):
    response = await admin_client.post(
        send_url(
            complaint.id,
            complaint_response_draft.id,
        )
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["id"] == complaint_response_draft.id
    assert data["complaint_id"] == complaint.id
    assert data["status"] == ComplaintResponseStatus.SENT.value

    assert data["external_message_id"] == (
        fake_mail_service.external_id
    )

    assert data["sent_at"] is not None
    assert data["delivered_at"] is None

    assert len(fake_mail_service.sent) == 1


async def test_send_response_mail_payload_e2e(
    admin_client: AsyncClient,
    complaint,
    complaint_response_draft,
    fake_mail_service,
):
    response = await admin_client.post(
        send_url(
            complaint.id,
            complaint_response_draft.id,
        )
    )

    assert response.status_code == 200, response.text
    assert len(fake_mail_service.sent) == 1

    mail = fake_mail_service.sent[0]

    assert mail.to == complaint.email

    assert complaint.complaint_number in mail.subject
    assert complaint_response_draft.message in mail.html

    assert "CHOCCA" in mail.html


async def test_send_response_persists_state_e2e(
    admin_client: AsyncClient,
    db_session,
    complaint,
    complaint_response_draft,
    fake_mail_service,
):
    response = await admin_client.post(
        send_url(
            complaint.id,
            complaint_response_draft.id,
        )
    )

    assert response.status_code == 200, response.text

    saved_complaint, saved_response = await load_saved_state(
        db_session,
        complaint_id=complaint.id,
        response_id=complaint_response_draft.id,
    )

    assert saved_complaint.status == ComplaintStatus.RESPONDED
    assert saved_complaint.responded_at is not None

    assert saved_response.status == ComplaintResponseStatus.SENT

    assert saved_response.external_message_id == (
        fake_mail_service.external_id
    )

    assert saved_response.sent_at is not None
    assert saved_response.delivered_at is None

    assert saved_response.error_message is None


async def test_send_response_preserves_original_content_e2e(
    admin_client: AsyncClient,
    db_session,
    complaint,
    complaint_response_draft,
):
    original_message = complaint_response_draft.message
    original_author = complaint_response_draft.author_user_id

    response = await admin_client.post(
        send_url(
            complaint.id,
            complaint_response_draft.id,
        )
    )

    assert response.status_code == 200, response.text

    _, saved = await load_saved_state(
        db_session,
        complaint_id=complaint.id,
        response_id=complaint_response_draft.id,
    )

    assert saved.message == original_message
    assert saved.author_user_id == original_author
    assert saved.recipient_email == complaint.email


# ============================================================
# BUSINESS RULES
# ============================================================

async def test_send_response_carta_rejected_e2e(
    admin_client: AsyncClient,
    db_session,
    complaint_carta,
    admin_user,
    fake_mail_service,
):
    draft = ComplaintResponseTable(
        complaint_id=complaint_carta.id,
        author_user_id=admin_user["user"].id,
        message=(
            "Se comunica la respuesta formal "
            "mediante correspondencia física."
        ),
        status=ComplaintResponseStatus.DRAFT,
        recipient_email=None,
    )

    db_session.add(draft)
    await db_session.commit()
    await db_session.refresh(draft)

    response = await admin_client.post(
        send_url(
            complaint_carta.id,
            draft.id,
        )
    )

    assert response.status_code in (400, 409), response.text

    assert len(fake_mail_service.sent) == 0

    saved_complaint, saved_response = await load_saved_state(
        db_session,
        complaint_id=complaint_carta.id,
        response_id=draft.id,
    )

    assert saved_complaint.status == ComplaintStatus.SUBMITTED
    assert saved_response.status == ComplaintResponseStatus.DRAFT


async def test_send_response_duplicate_rejected_e2e(
    admin_client: AsyncClient,
    complaint,
    complaint_response_draft,
    fake_mail_service,
):
    url = send_url(
        complaint.id,
        complaint_response_draft.id,
    )

    first = await admin_client.post(url)

    assert first.status_code == 200, first.text
    assert len(fake_mail_service.sent) == 1

    second = await admin_client.post(url)

    assert second.status_code in (400, 409), second.text

    # Lo importante: nunca debió enviarse dos veces.
    assert len(fake_mail_service.sent) == 1


async def test_send_response_wrong_complaint_e2e(
    admin_client: AsyncClient,
    another_complaint,
    complaint_response_draft,
    fake_mail_service,
):
    response = await admin_client.post(
        send_url(
            another_complaint.id,
            complaint_response_draft.id,
        )
    )

    assert response.status_code in (400, 404, 409), response.text

    assert len(fake_mail_service.sent) == 0


async def test_send_response_already_responded_rejected_e2e(
    admin_client: AsyncClient,
    complaint_responded,
    complaint_response_sent,
    fake_mail_service,
):
    response = await admin_client.post(
        send_url(
            complaint_responded.id,
            complaint_response_sent.id,
        )
    )

    assert response.status_code in (400, 409), response.text
    assert len(fake_mail_service.sent) == 0


async def test_send_response_not_found_e2e(
    admin_client: AsyncClient,
    complaint,
    fake_mail_service,
):
    response = await admin_client.post(
        send_url(
            complaint.id,
            999999999,
        )
    )

    assert response.status_code == 404
    assert len(fake_mail_service.sent) == 0


@pytest.mark.parametrize(
    "complaint_id,response_id",
    [
        (0, 1),
        (1, 0),
        (-1, 1),
        (1, -1),
    ],
)
async def test_send_response_invalid_ids_e2e(
    admin_client: AsyncClient,
    complaint_id,
    response_id,
    fake_mail_service,
):
    response = await admin_client.post(
        send_url(complaint_id, response_id)
    )

    assert response.status_code == 422, response.text
    assert len(fake_mail_service.sent) == 0


async def test_send_response_provider_failure_e2e(
    admin_client: AsyncClient,
    db_session,
    complaint,
    complaint_response_draft,
    fake_mail_service,
):
    fake_mail_service.fail_with = TimeoutError(
        "Simulated provider timeout"
    )

    response = await admin_client.post(
        send_url(
            complaint.id,
            complaint_response_draft.id,
        )
    )

    # Contrato actual:
    # el error de Resend se propaga y el middleware
    # lo convierte en 500.
    assert response.status_code == 500, response.text

    assert len(fake_mail_service.sent) == 1

    saved_complaint, saved_response = await load_saved_state(
        db_session,
        complaint_id=complaint.id,
        response_id=complaint_response_draft.id,
    )

    assert saved_complaint.status == ComplaintStatus.SUBMITTED
    assert saved_complaint.responded_at is None

    assert (
        saved_response.status
        == ComplaintResponseStatus.PENDING_SEND
    )

    assert saved_response.external_message_id is None
    assert saved_response.sent_at is None


async def test_send_response_pending_cannot_resend_e2e(
    admin_client: AsyncClient,
    db_session,
    complaint,
    complaint_response_draft,
    fake_mail_service,
):
    fake_mail_service.fail_with = TimeoutError(
        "Simulated provider timeout"
    )

    url = send_url(
        complaint.id,
        complaint_response_draft.id,
    )

    first = await admin_client.post(url)

    assert first.status_code == 500, first.text
    assert len(fake_mail_service.sent) == 1

    # Quitamos el fallo simulado.
    fake_mail_service.fail_with = None

    second = await admin_client.post(url)

    assert second.status_code in (400, 409), second.text

    # El sistema no debe reintentar automáticamente
    # sin resolver primero el envío incierto.
    assert len(fake_mail_service.sent) == 1

async def test_send_response_requires_auth_e2e(
    http_client: AsyncClient,
    complaint,
    complaint_response_draft,
    fake_mail_service,
):
    http_client.cookies.clear()

    response = await http_client.post(
        send_url(
            complaint.id,
            complaint_response_draft.id,
        )
    )

    assert response.status_code in (401, 403)
    assert len(fake_mail_service.sent) == 0
