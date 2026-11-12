from copy import deepcopy
from uuid import uuid4
from decimal import Decimal

import pytest
from httpx import AsyncClient
from sqlalchemy import select, text, func

from app.features.complaints.models.complaint import (
    ComplaintTable,
)
from app.features.orders.models.order import OrderTable



pytestmark = pytest.mark.asyncio(
    loop_scope="session",
)

SQL_PAYLOADS = [
    "' OR '1'='1",
    "' OR 1=1 --",
    "'; DROP TABLE customer; --",
    "' UNION SELECT NULL --",
]

async def count_orders(db_session) -> int:
    result = await db_session.execute(
        select(func.count()).select_from(OrderTable)
    )
    return result.scalar_one()

async def assert_database_intact(db_session):

    for table_name in (
        "usertable",
        "customer",
        "orders",
        "product",
    ):
        result = await db_session.execute(
            text("""
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_schema = current_schema()
                      AND table_name = :table_name
                )
            """),
            {"table_name": table_name},
        )

        assert result.scalar_one() is True, (
            f"Critical table missing: {table_name}"
        )


@pytest.mark.parametrize("injection", SQL_PAYLOADS)
async def test_login_sql_injection_e2e(
    http_client: AsyncClient,
    admin_user,
    db_session,
    injection,
):
    http_client.cookies.clear()

    response = await http_client.post(
        "/auth/login",
        json={
            "email": admin_user["user"].email,
            "password": injection,
        },
    )

    assert response.status_code in (
        400,
        401,
        403,
        422,
    ), response.text

    assert not http_client.cookies.get(
        "session_token"
    )

    await assert_database_intact(db_session)



@pytest.mark.parametrize(
    "injection",
    [
        "' OR '1'='1",
        "admin@test.com' OR '1'='1",
    ],
)
async def test_login_email_injection_e2e(
    http_client: AsyncClient,
    db_session,
    injection,
):
    http_client.cookies.clear()

    response = await http_client.post(
        "/auth/login",
        json={
            "email": injection,
            "password": "InvalidPassword123!",
        },
    )

    assert response.status_code in (
        400,
        401,
        403,
        422,
    ), response.text

    assert not http_client.cookies.get(
        "session_token"
    )

    await assert_database_intact(db_session)


@pytest.mark.parametrize("injection", SQL_PAYLOADS)
async def test_complaint_detail_sql_injection_e2e(
    http_client: AsyncClient,
    db_session,
    complaint_payload,
    fake_mail_service,
    injection,
):
    http_client.cookies.clear()

    payload = deepcopy(complaint_payload)

    payload["detail"] = (
        f"Reclamo de prueba: {injection}"
    )

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

    assert complaint.detail == payload["detail"]

    await assert_database_intact(db_session)

@pytest.mark.parametrize("injection", SQL_PAYLOADS)
async def test_complaint_solution_sql_injection_e2e(
    http_client: AsyncClient,
    db_session,
    complaint_payload,
    fake_mail_service,
    injection,
):
    http_client.cookies.clear()

    payload = deepcopy(complaint_payload)

    payload["requested_solution"] = (
        f"Solicito una solucion: {injection}"
    )

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

    assert (
        complaint.requested_solution
        == payload["requested_solution"]
    )

    await assert_database_intact(db_session)

@pytest.mark.parametrize("injection", SQL_PAYLOADS)
async def test_complaint_order_number_sql_injection_e2e(
    http_client: AsyncClient,
    db_session,
    complaint_payload,
    fake_mail_service,
    injection,
):
    http_client.cookies.clear()

    payload = deepcopy(complaint_payload)
    payload["order_number"] = injection

    response = await http_client.post(
        "/complaints",
        json=payload,
    )

    assert response.status_code in (
        201,
        400,
        422,
    ), response.text

    if response.status_code == 201:
        result = await db_session.execute(
            select(ComplaintTable).where(
                ComplaintTable.complaint_number
                == response.json()["complaint_number"]
            )
        )

        complaint = result.scalar_one()

        assert complaint.order_number == injection

    await assert_database_intact(db_session)

@pytest.mark.parametrize("injection", SQL_PAYLOADS)
async def test_order_coupon_sql_injection_e2e(
    admin_client: AsyncClient,
    db_session,
    wholesale_cart,
    location,
    injection,
):
    before = await count_orders(db_session)

    response = await admin_client.post(
        "/orders",
        json={
            "delivery_method": "STORE_PICKUP",
            "pickup": {
                "location_id": location.id,
            },
            "payment_method": "CASH",
            "coupon_code": injection,
        },
    )

    assert response.status_code in (
        201, 400, 404, 422
    ), response.text

    after = await count_orders(db_session)

    if response.status_code == 201:
        assert after == before + 1

        result = await db_session.execute(
            select(OrderTable)
            .order_by(OrderTable.id.desc())
            .limit(1)
        )

        order = result.scalar_one()

        assert order.discount_amount == Decimal("0.00")
        assert order.total > Decimal("0.00")
    else:
        assert after == before



async def test_register_name_sql_injection_e2e(
    http_client: AsyncClient,
    db_session,
    bypass_captcha,
):
    http_client.cookies.clear()

    injection = "'; DROP TABLE usertable; --"

    email = f"security-{uuid4().hex}@test.com"

    response = await http_client.post(
        "/auth/register",
        json={
            "name": injection,
            "email": email,
            "password": "StrongPassword123!",
            "captchaToken": "e2e-captcha-bypass",
            "accepted_terms": True
        },
    )

    assert response.status_code in (
        201, 400, 422
    ), response.text

    result = await db_session.execute(
        text("""
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_schema = current_schema()
                  AND table_name = 'usertable'
            )
        """)
    )

    assert result.scalar_one() is True

    if response.status_code == 201:
        result = await db_session.execute(
            text("""
                SELECT nombre
                FROM usertable
                WHERE email = :email
            """),
            {"email": email},
        )

        assert result.scalar_one() == injection