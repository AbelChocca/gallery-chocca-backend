
from decimal import Decimal
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import text

from app.features.orders.types.order import OrderStatus
from app.features.orders.types.delivery import DeliveryMethod
from app.features.payments.types.payment import PaymentMethod
from app.features.customer.customer_types import CustomerType


pytestmark = pytest.mark.asyncio(
    loop_scope="session",
)

ORDERS_URL = "/order/me"


async def login_as(
    client: AsyncClient,
    *,
    email: str,
    password: str,
):
    client.cookies.clear()

    response = await client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 200, response.text


async def insert_customer(
    db_session,
    *,
    user_id: int,
    name: str,
):
    result = await db_session.execute(
        text("""
            INSERT INTO customer (
                user_id,
                session_id,
                customer_type,
                name,
                last_name,
                email,
                created_at,
                updated_at
            )
            VALUES (
                :user_id,
                NULL,
                :customer_type,
                :name,
                'Testing',
                :email,
                NOW(),
                NOW()
            )
            RETURNING id
        """),
        {
            "user_id": user_id,
            # PostgreSQL ENUM(CustomerType) almacena
            # normalmente el nombre del miembro.
            "customer_type": CustomerType.REGULAR.name,
            "name": name,
            "email": f"{uuid4().hex}@test.com",
        },
    )

    return result.scalar_one()


async def insert_order(
    db_session,
    *,
    customer_id: int | None,
    status: OrderStatus = OrderStatus.PENDING_PAYMENT,
    total: str = "109.90",
):
    order_number = f"GC-E2E-{uuid4().hex[:12]}"

    result = await db_session.execute(
        text("""
            INSERT INTO orders (
                order_number,
                customer_id,
                payment_method,
                status,
                delivery_method,
                subtotal,
                discount_amount,
                shipping_cost,
                total,
                created_at,
                updated_at
            )
            VALUES (
                :order_number,
                :customer_id,
                :payment_method,
                :status,
                :delivery_method,
                :subtotal,
                0.00,
                0.00,
                :total,
                NOW(),
                NOW()
            )
            RETURNING id
        """),
        {
            "order_number": order_number,
            "customer_id": customer_id,
            "payment_method": PaymentMethod.CARD.value,
            "status": status.value,
            "delivery_method": DeliveryMethod.SHIPPING.value,
            "subtotal": total,
            "total": total,
        },
    )

    return {
        "id": result.scalar_one(),
        "order_number": order_number,
    }


async def insert_order_item(
    db_session,
    *,
    order_id: int,
    product_name: str,
    quantity: int = 1,
    unit_price: str = "109.90",
):
    price = Decimal(unit_price)
    total = price * quantity

    await db_session.execute(
        text("""
            INSERT INTO order_items (
                order_id,
                product_id,
                variant_id,
                variant_size_id,
                product_name,
                sku,
                color,
                size,
                quantity,
                unit_original_price,
                unit_final_price,
                discount_amount,
                original_total,
                final_total
            )
            VALUES (
                :order_id,
                NULL,
                NULL,
                NULL,
                :product_name,
                :sku,
                'BLACK',
                'M',
                :quantity,
                :unit_price,
                :unit_price,
                0.00,
                :total,
                :total
            )
        """),
        {
            "order_id": order_id,
            "product_name": product_name,
            "sku": f"SKU-{uuid4().hex[:10]}",
            "quantity": quantity,
            "unit_price": price,
            "total": total,
        },
    )


async def get_my_orders(
    client: AsyncClient,
):
    response = await client.get(ORDERS_URL)

    assert response.status_code == 200, response.text

    return response.json()


@pytest_asyncio.fixture(
    scope="function",
    loop_scope="session",
)
async def two_users(
    db_session,
    admin_user,
):
    user_a = admin_user["user"]
    password = admin_user["password"]

    # Creamos un segundo usuario con el mismo rol,
    # pero identidad y user_id completamente distintos.
    UserModel = type(user_a)

    user_b = UserModel(
        nombre="admin-security-b",
        email=f"admin-b-{uuid4().hex}@test.com",
        role=user_a.role,
        hashed_password=user_a.hashed_password,
        is_active=True,
    )

    db_session.add(user_b)

    await db_session.commit()
    await db_session.refresh(user_b)

    assert user_a.id != user_b.id

    return {
        "a": user_a,
        "b": user_b,
        "password": password,
    }


# =========================================================
# FIXTURE: PEDIDOS DE A, B Y SIN PROPIETARIO
# =========================================================

@pytest_asyncio.fixture(
    scope="function",
    loop_scope="session",
)
async def ownership_data(
    db_session,
    two_users,
):
    customer_a = await insert_customer(
        db_session,
        user_id=two_users["a"].id,
        name="Customer A",
    )

    customer_b = await insert_customer(
        db_session,
        user_id=two_users["b"].id,
        name="Customer B",
    )

    # Usuario A: dos pedidos.
    order_a1 = await insert_order(
        db_session,
        customer_id=customer_a,
    )

    order_a2 = await insert_order(
        db_session,
        customer_id=customer_a,
        status=OrderStatus.CONFIRMED,
        total="159.90",
    )

    # Usuario B: un pedido.
    order_b1 = await insert_order(
        db_session,
        customer_id=customer_b,
        total="79.90",
    )

    # Pedido sin propietario.
    orphan_order = await insert_order(
        db_session,
        customer_id=None,
        total="49.90",
    )

    await insert_order_item(
        db_session,
        order_id=order_a1["id"],
        product_name="Jean Exclusivo A",
    )

    await insert_order_item(
        db_session,
        order_id=order_a2["id"],
        product_name="Jean Segundo A",
        unit_price="159.90",
    )

    await insert_order_item(
        db_session,
        order_id=order_b1["id"],
        product_name="Jean Privado B",
        unit_price="79.90",
    )

    await insert_order_item(
        db_session,
        order_id=orphan_order["id"],
        product_name="Jean Sin Propietario",
        unit_price="49.90",
    )

    await db_session.commit()

    return {
        **two_users,
        "customer_a": customer_a,
        "customer_b": customer_b,
        "orders_a": [order_a1, order_a2],
        "orders_b": [order_b1],
        "orphan_order": orphan_order,
    }


# =========================================================
# 1. USUARIO A SOLO VE SUS PEDIDOS
# =========================================================

async def test_user_a_only_sees_own_orders_e2e(
    http_client: AsyncClient,
    ownership_data,
):
    await login_as(
        http_client,
        email=ownership_data["a"].email,
        password=ownership_data["password"],
    )

    orders = await get_my_orders(http_client)

    returned_ids = {order["id"] for order in orders}
    expected_ids = {
        order["id"]
        for order in ownership_data["orders_a"]
    }

    assert returned_ids == expected_ids
    assert len(orders) == 2

    assert ownership_data["orders_b"][0]["id"] not in returned_ids


# =========================================================
# 2. USUARIO B NO VE PEDIDOS DE A
# =========================================================

async def test_user_b_cannot_see_user_a_orders_e2e(
    http_client: AsyncClient,
    ownership_data,
):
    await login_as(
        http_client,
        email=ownership_data["b"].email,
        password=ownership_data["password"],
    )

    orders = await get_my_orders(http_client)

    returned_ids = {order["id"] for order in orders}

    assert returned_ids == {
        ownership_data["orders_b"][0]["id"]
    }

    for order in ownership_data["orders_a"]:
        assert order["id"] not in returned_ids


# =========================================================
# 3. LOS ITEMS TAMBIÉN SON PRIVADOS
# =========================================================

async def test_order_items_are_owner_scoped_e2e(
    http_client: AsyncClient,
    ownership_data,
):
    await login_as(
        http_client,
        email=ownership_data["a"].email,
        password=ownership_data["password"],
    )

    orders = await get_my_orders(http_client)

    product_names = {
        item["product_name"]
        for order in orders
        for item in order["items"]
    }

    assert product_names == {
        "Jean Exclusivo A",
        "Jean Segundo A",
    }

    assert "Jean Privado B" not in product_names
    assert "Jean Sin Propietario" not in product_names


# =========================================================
# 4. CAMBIAR DE SESIÓN NO FILTRA PEDIDOS
# =========================================================

async def test_switching_users_does_not_leak_orders_e2e(
    http_client: AsyncClient,
    ownership_data,
):
    for key, expected_orders in (
        ("a", ownership_data["orders_a"]),
        ("b", ownership_data["orders_b"]),
        ("a", ownership_data["orders_a"]),
    ):
        await login_as(
            http_client,
            email=ownership_data[key].email,
            password=ownership_data["password"],
        )

        orders = await get_my_orders(http_client)

        assert {order["id"] for order in orders} == {
            order["id"] for order in expected_orders
        }


# =========================================================
# 5. PEDIDOS SIN CUSTOMER_ID NO SE FILTRAN
# =========================================================

async def test_orphan_order_is_not_exposed_e2e(
    http_client: AsyncClient,
    ownership_data,
):
    orphan_id = ownership_data["orphan_order"]["id"]

    for user_key in ("a", "b"):
        await login_as(
            http_client,
            email=ownership_data[user_key].email,
            password=ownership_data["password"],
        )

        orders = await get_my_orders(http_client)

        assert orphan_id not in {
            order["id"] for order in orders
        }


# =========================================================
# 6. USUARIO SIN CUSTOMER RECIBE LISTA VACÍA
# =========================================================

async def test_user_without_customer_gets_empty_orders_e2e(
    http_client: AsyncClient,
    admin_user,
):
    await login_as(
        http_client,
        email=admin_user["user"].email,
        password=admin_user["password"],
    )

    orders = await get_my_orders(http_client)

    assert orders == []


# =========================================================
# 7. CUSTOMER SIN PEDIDOS RECIBE LISTA VACÍA
# =========================================================

async def test_customer_without_orders_gets_empty_list_e2e(
    http_client: AsyncClient,
    db_session,
    admin_user,
):
    await insert_customer(
        db_session,
        user_id=admin_user["user"].id,
        name="Empty Customer",
    )

    await db_session.commit()

    await login_as(
        http_client,
        email=admin_user["user"].email,
        password=admin_user["password"],
    )

    orders = await get_my_orders(http_client)

    assert orders == []
