
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from types import SimpleNamespace
from uuid import uuid4

import pytest
import pytest_asyncio

from app.features.complaints.models.complaint import ComplaintTable
from app.features.complaints.models.complaint_response import (
    ComplaintResponseTable,
)

from app.features.complaints.types.complaint import (
    ComplaintType,
    ComplaintGoodType,
    ComplaintDocumentType,
    ComplaintResponseChannel,
    ComplaintStatus,
)

from app.features.complaints.types.complaint_response import (
    ComplaintResponseStatus,
)

from app.features.mail.services.mail_service import MailService


def unique_complaint_number() -> str:
    return f"LR-2026-{uuid4().int % 1_000_000:06d}"


def build_complaint_model(
    *,
    response_channel: ComplaintResponseChannel = (
        ComplaintResponseChannel.EMAIL
    ),
    status: ComplaintStatus = ComplaintStatus.SUBMITTED,
    **overrides,
) -> ComplaintTable:
    now = datetime.now(timezone.utc)
    suffix = uuid4().hex[:8]

    data = {
        "public_id": uuid4(),
        "complaint_number": unique_complaint_number(),

        "provider_legal_name": "OLD DENIM CLUB TEST",
        "provider_ruc": "00000000000",
        "provider_address": "Direccion fiscal de pruebas",

        "first_name": "Cliente",
        "last_name": f"E2E-{suffix}",
        "document_type": ComplaintDocumentType.DNI,
        "document_number": "12345678",
        "email": f"cliente-{suffix}@example.com",
        "phone": "999999999",
        "address": "Av. Pruebas 123, Lima",

        "is_minor": False,
        "representative_name": None,
        "representative_document": None,

        "good_type": ComplaintGoodType.PRODUCTO,
        "order_number": None,
        "amount": Decimal("150.00"),
        "product_description": "Jean BGOO de prueba",

        "complaint_type": ComplaintType.RECLAMO,
        "detail": (
            "El producto recibido presenta un defecto "
            "que impide utilizarlo correctamente."
        ),
        "requested_solution": (
            "Solicito el cambio del producto "
            "por uno en buen estado."
        ),

        "response_channel": response_channel,
        "status": status,

        "created_at": now,
        "updated_at": now,
        "response_due_at": now + timedelta(days=21),
        "responded_at": (
            now if status == ComplaintStatus.RESPONDED else None
        ),
    }

    data.update(overrides)

    return ComplaintTable(**data)


async def persist_complaint(
    db_session,
    **kwargs,
) -> ComplaintTable:
    complaint = build_complaint_model(**kwargs)

    db_session.add(complaint)
    await db_session.commit()
    await db_session.refresh(complaint)

    return complaint


async def persist_complaint_response(
    db_session,
    *,
    complaint_id: int,
    author_user_id: int,
    status: ComplaintResponseStatus = (
        ComplaintResponseStatus.DRAFT
    ),
    message: str = (
        "Hemos evaluado su reclamación y procederemos "
        "con la solución solicitada."
    ),
    recipient_email: str | None = None,
) -> ComplaintResponseTable:
    now = datetime.now(timezone.utc)

    response = ComplaintResponseTable(
        complaint_id=complaint_id,
        author_user_id=author_user_id,
        message=message,
        status=status,
        recipient_email=recipient_email,
        external_message_id=(
            f"email_test_{uuid4().hex}"
            if status == ComplaintResponseStatus.SENT
            else None
        ),
        error_message=None,
        physical_delivery_reference=None,
        created_at=now,
        sent_at=(
            now if status == ComplaintResponseStatus.SENT else None
        ),
        delivered_at=None,
    )

    db_session.add(response)
    await db_session.commit()
    await db_session.refresh(response)

    return response


# ============================================================
# PUBLIC CREATE PAYLOAD
# ============================================================

@pytest.fixture
def complaint_payload():
    suffix = uuid4().hex[:8]

    return {
        "first_name": "Juan",
        "last_name": "Perez",
        "document_type": ComplaintDocumentType.DNI.value,
        "document_number": "12345678",
        "email": f"cliente-{suffix}@example.com",
        "phone": "999999999",
        "address": "Av. Ejemplo 123, Lima",

        "is_minor": False,

        "good_type": ComplaintGoodType.PRODUCTO.value,
        "order_number": None,
        "amount": "150.00",
        "product_description": "Jean BGOO talla 32",

        "complaint_type": ComplaintType.RECLAMO.value,
        "detail": (
            "El producto recibido tiene un defecto "
            "en la costura lateral."
        ),
        "requested_solution": (
            "Solicito el cambio del producto "
            "por uno sin defectos."
        ),
        "response_channel": ComplaintResponseChannel.EMAIL.value,
    }


# ============================================================
# COMPLAINT FIXTURES
# ============================================================

@pytest_asyncio.fixture(
    scope="function",
    loop_scope="session",
)
async def complaint(db_session):
    return await persist_complaint(db_session)


@pytest_asyncio.fixture(
    scope="function",
    loop_scope="session",
)
async def another_complaint(db_session):
    return await persist_complaint(
        db_session,
        complaint_type=ComplaintType.QUEJA,
    )


@pytest_asyncio.fixture(
    scope="function",
    loop_scope="session",
)
async def complaint_carta(db_session):
    return await persist_complaint(
        db_session,
        response_channel=ComplaintResponseChannel.CARTA,
        email=None,
    )


@pytest_asyncio.fixture(
    scope="function",
    loop_scope="session",
)
async def complaint_responded(db_session):
    return await persist_complaint(
        db_session,
        status=ComplaintStatus.RESPONDED,
    )


# ============================================================
# COMPLAINT RESPONSE FIXTURES
# ============================================================

@pytest_asyncio.fixture(
    scope="function",
    loop_scope="session",
)
async def complaint_response_draft(
    db_session,
    complaint,
    admin_user,
):
    return await persist_complaint_response(
        db_session,
        complaint_id=complaint.id,
        author_user_id=admin_user["user"].id,
        recipient_email=complaint.email,
    )


@pytest_asyncio.fixture(
    scope="function",
    loop_scope="session",
)
async def complaint_response_sent(
    db_session,
    complaint_responded,
    admin_user,
):
    return await persist_complaint_response(
        db_session,
        complaint_id=complaint_responded.id,
        author_user_id=admin_user["user"].id,
        status=ComplaintResponseStatus.SENT,
        recipient_email=complaint_responded.email,
    )


@pytest_asyncio.fixture(
    scope="function",
    loop_scope="session",
)
async def complaint_responses(
    db_session,
    complaint,
    admin_user,
):
    first = await persist_complaint_response(
        db_session,
        complaint_id=complaint.id,
        author_user_id=admin_user["user"].id,
        message=(
            "Estamos revisando su reclamación "
            "y verificando la información recibida."
        ),
        recipient_email=complaint.email,
    )

    second = await persist_complaint_response(
        db_session,
        complaint_id=complaint.id,
        author_user_id=admin_user["user"].id,
        message=(
            "Hemos finalizado la evaluación "
            "y preparado una respuesta."
        ),
        recipient_email=complaint.email,
    )

    return [first, second]

@pytest.fixture(scope="function")
def fake_mail_service(monkeypatch):

    fake = SimpleNamespace(
        sent=[],
        fail_with=None,
        external_id=f"email_test_{uuid4().hex}",
    )

    async def fake_send(self, *, payload):
        fake.sent.append(payload)

        if fake.fail_with is not None:
            raise fake.fail_with

        return SimpleNamespace(id=fake.external_id)

    monkeypatch.setattr(
        MailService,
        "send",
        fake_send,
    )

    return fake
