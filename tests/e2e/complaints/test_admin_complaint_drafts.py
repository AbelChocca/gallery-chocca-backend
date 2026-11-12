
import pytest

from httpx import AsyncClient
from sqlalchemy import select

from app.features.complaints.models.complaint_response import (
    ComplaintResponseTable,
)
from app.features.complaints.types.complaint_response import (
    ComplaintResponseStatus,
)


pytestmark = pytest.mark.asyncio(
    loop_scope="session",
)



async def test_create_draft_success_e2e(
    admin_client: AsyncClient,
    db_session,
    complaint,
    admin_user,
):
    complaint_id = complaint.id
    admin_id = admin_user["user"].id

    message = (
        "Hemos revisado su reclamación y estamos "
        "evaluando la solución solicitada."
    )

    response = await admin_client.post(
        f"/complaints/admin/{complaint_id}/responses",
        json={"message": message},
    )

    assert response.status_code == 201, response.text

    data = response.json()

    assert data["complaint_id"] == complaint_id
    assert data["author_user_id"] == admin_id
    assert data["message"] == message
    assert data["status"] == ComplaintResponseStatus.DRAFT.value
    assert data["recipient_email"] == complaint.email

    assert data["external_message_id"] is None
    assert data["sent_at"] is None
    assert data["delivered_at"] is None

    result = await db_session.execute(
        select(ComplaintResponseTable)
        .where(
            ComplaintResponseTable.id == data["id"]
        )
        .execution_options(populate_existing=True)
    )

    saved = result.scalar_one()

    assert saved.complaint_id == complaint_id
    assert saved.author_user_id == admin_id
    assert saved.status == ComplaintResponseStatus.DRAFT
    assert saved.message == message


async def test_create_draft_for_carta_e2e(
    admin_client: AsyncClient,
    complaint_carta,
):
    response = await admin_client.post(
        f"/complaints/admin/{complaint_carta.id}/responses",
        json={
            "message": (
                "Se ha evaluado su reclamación. "
                "La respuesta será comunicada por carta."
            )
        },
    )

    assert response.status_code == 201, response.text

    data = response.json()

    assert data["status"] == ComplaintResponseStatus.DRAFT.value
    assert data["recipient_email"] is None


async def test_create_draft_not_found_e2e(
    admin_client: AsyncClient,
):
    response = await admin_client.post(
        "/complaints/admin/999999999/responses",
        json={
            "message": (
                "Respuesta de prueba para una reclamación "
                "que no existe."
            )
        },
    )

    assert response.status_code == 404


async def test_create_draft_responded_complaint_e2e(
    admin_client: AsyncClient,
    complaint_responded,
):
    response = await admin_client.post(
        f"/complaints/admin/{complaint_responded.id}/responses",
        json={
            "message": (
                "Intento de crear un borrador en una "
                "reclamación ya respondida."
            )
        },
    )

    assert response.status_code in (400, 409), response.text


@pytest.mark.parametrize(
    "message",
    [
        "",
        "corto",
        " ",
        "a" * 10001,
    ],
)
async def test_create_draft_invalid_message_e2e(
    admin_client: AsyncClient,
    complaint,
    message,
):
    response = await admin_client.post(
        f"/complaints/admin/{complaint.id}/responses",
        json={"message": message},
    )

    assert response.status_code == 422, response.text


async def test_create_draft_requires_auth_e2e(
    http_client: AsyncClient,
    complaint,
):
    http_client.cookies.clear()

    response = await http_client.post(
        f"/complaints/admin/{complaint.id}/responses",
        json={
            "message": (
                "Intento de creación sin autorización "
                "administrativa."
            )
        },
    )

    assert response.status_code in (401, 403)


async def test_update_draft_success_e2e(
    admin_client: AsyncClient,
    db_session,
    complaint,
    complaint_response_draft,
):
    # Capturamos los IDs antes de expirar entidades.
    complaint_id = complaint.id
    response_id = complaint_response_draft.id

    new_message = (
        "Después de revisar la información, "
        "hemos aprobado el cambio del producto."
    )

    response = await admin_client.patch(
        (
            f"/complaints/admin/{complaint_id}"
            f"/responses/{response_id}"
        ),
        json={"message": new_message},
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["id"] == response_id
    assert data["message"] == new_message
    assert data["status"] == ComplaintResponseStatus.DRAFT.value

    # Limpiar atributos cacheados.
    db_session.expire_all()

    # Usamos el ID guardado, no el objeto expirado.
    result = await db_session.execute(
        select(ComplaintResponseTable).where(
            ComplaintResponseTable.id == response_id
        )
    )

    saved = result.scalar_one()

    assert saved.message == new_message
    assert saved.status == ComplaintResponseStatus.DRAFT


async def test_update_draft_wrong_complaint_e2e(
    admin_client: AsyncClient,
    another_complaint,
    complaint_response_draft,
):
    response = await admin_client.patch(
        (
            f"/complaints/admin/{another_complaint.id}"
            f"/responses/{complaint_response_draft.id}"
        ),
        json={
            "message": (
                "No debe poder editarse esta respuesta "
                "desde otra reclamación."
            )
        },
    )

    assert response.status_code in (400, 404, 409), response.text


async def test_update_sent_response_rejected_e2e(
    admin_client: AsyncClient,
    complaint_responded,
    complaint_response_sent,
):
    response = await admin_client.patch(
        (
            f"/complaints/admin/{complaint_responded.id}"
            f"/responses/{complaint_response_sent.id}"
        ),
        json={
            "message": (
                "Intento de modificar una respuesta "
                "formal que ya fue enviada."
            )
        },
    )

    assert response.status_code in (400, 409), response.text


async def test_update_draft_responded_complaint_e2e(
    admin_client: AsyncClient,
    complaint_responded,
    db_session,
    admin_user,
):
    response_model = ComplaintResponseTable(
        complaint_id=complaint_responded.id,
        author_user_id=admin_user["user"].id,
        message="Borrador previo de prueba.",
        status=ComplaintResponseStatus.DRAFT,
        recipient_email=complaint_responded.email,
    )

    db_session.add(response_model)
    await db_session.commit()
    await db_session.refresh(response_model)

    response = await admin_client.patch(
        (
            f"/complaints/admin/{complaint_responded.id}"
            f"/responses/{response_model.id}"
        ),
        json={
            "message": (
                "No debería permitirse editar cuando "
                "la reclamación ya fue respondida."
            )
        },
    )

    assert response.status_code in (400, 409), response.text


@pytest.mark.parametrize(
    "message",
    [
        "",
        "a",
        " ",
        "a" * 10001,
    ],
)
async def test_update_draft_invalid_message_e2e(
    admin_client: AsyncClient,
    complaint,
    complaint_response_draft,
    message,
):
    response = await admin_client.patch(
        (
            f"/complaints/admin/{complaint.id}"
            f"/responses/{complaint_response_draft.id}"
        ),
        json={"message": message},
    )

    assert response.status_code == 422, response.text


async def test_update_draft_requires_auth_e2e(
    http_client: AsyncClient,
    complaint,
    complaint_response_draft,
):
    http_client.cookies.clear()

    response = await http_client.patch(
        (
            f"/complaints/admin/{complaint.id}"
            f"/responses/{complaint_response_draft.id}"
        ),
        json={
            "message": (
                "Intento de editar una respuesta "
                "sin estar autenticado."
            )
        },
    )

    assert response.status_code in (401, 403)
