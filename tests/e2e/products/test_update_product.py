
import io
import json
from decimal import Decimal
from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy import text

from app.features.products.schema import (
    CategoryType,
    BrandType,
    SizeType,
)


pytestmark = pytest.mark.asyncio(
    loop_scope="session",
)


# =========================================================
# HELPERS
# =========================================================

def unique_letters() -> str:
    value = uuid4().int
    letters = []

    for _ in range(12):
        value, remainder = divmod(value, 26)
        letters.append(chr(ord("a") + remainder))

    return "".join(letters)


@pytest.fixture
def update_product_payload(location):
    unique = unique_letters()

    return {
        "nombre": f"Jean Clasico {unique}",
        "descripcion": "Producto original para pruebas E2E",
        "category": next(iter(CategoryType)).value,
        "brand": next(iter(BrandType)).value,
        "fit": "SLIM",
        "base_price": "109.90",
        "variants": [
            {
                "color": "black",
                "temp_key": "variant-black",
                "sizes": [
                    {
                        "size": next(iter(SizeType)).value,
                        "barcode": f"E2E-{uuid4().hex[:8]}",
                        "inventories": [
                            {
                                "location_id": location.id,
                                "minimum_stock": "2.00",
                                "initial_stock": "10.00",
                                "unit_price": "109.90",
                            }
                        ],
                    }
                ],
            }
        ],
        "temp_keys": ["variant-black"],
    }


@pytest.fixture
async def created_product(
    admin_client: AsyncClient,
    update_product_payload,
    fake_product_media,
    fake_product_cache,
):
    response = await admin_client.post(
        "/product/publish/",
        data={
            "product_schema_json": json.dumps(
                update_product_payload
            ),
        },
        files=[
            (
                "files",
                (
                    "product.jpg",
                    io.BytesIO(b"fake-image-content"),
                    "image/jpeg",
                ),
            )
        ],
    )

    assert response.status_code == 201, response.text

    # Descartar las invalidaciones de creación.
    fake_product_cache["entities"].clear()
    fake_product_cache["entity"].clear()

    return response.json()


async def get_product(db_session, product_id: int):
    result = await db_session.execute(
        text("""
            SELECT
                id,
                nombre,
                descripcion,
                slug,
                brand,
                category,
                fit,
                base_price,
                is_active
            FROM product
            WHERE id = :product_id
        """),
        {"product_id": product_id},
    )

    product = result.mappings().one_or_none()

    assert product is not None

    return product


# =========================================================
# 1. ACTUALIZAR PRECIO BASE
# =========================================================

async def test_update_product_base_price_e2e(
    admin_client: AsyncClient,
    created_product,
    db_session,
    fake_product_cache,
):
    product_id = created_product["id"]

    response = await admin_client.patch(
        f"/product/{product_id}",
        data={
            "base_price": "129.90",
        },
    )

    assert response.status_code == 204, response.text
    assert response.content == b""

    product = await get_product(
        db_session,
        product_id,
    )

    assert product["base_price"] == Decimal("129.90")

    assert fake_product_cache["entities"] == ["product"]
    assert fake_product_cache["entity"] == [
        ("product", product_id)
    ]


# =========================================================
# 2. ACTUALIZACIÓN PARCIAL
# =========================================================

async def test_update_product_partial_e2e(
    admin_client: AsyncClient,
    created_product,
    update_product_payload,
    db_session,
):
    product_id = created_product["id"]

    response = await admin_client.patch(
        f"/product/{product_id}",
        data={
            "descripcion": "Nueva descripcion del producto",
        },
    )

    assert response.status_code == 204, response.text

    product = await get_product(
        db_session,
        product_id,
    )

    assert product["descripcion"] == (
        "Nueva descripcion del producto"
    )

    # Campos no enviados deben permanecer iguales.
    assert product["nombre"] == (
        update_product_payload["nombre"]
    )
    assert product["base_price"] == Decimal("109.90")
    assert product["slug"] == created_product["slug"]


# =========================================================
# 3. CAMBIAR NOMBRE Y REGENERAR SLUG
# =========================================================

async def test_update_product_name_changes_slug_e2e(
    admin_client: AsyncClient,
    created_product,
    db_session,
):
    product_id = created_product["id"]
    old_slug = created_product["slug"]

    new_name = f"Jean Moderno {unique_letters()}"

    response = await admin_client.patch(
        f"/product/{product_id}",
        data={
            "nombre": new_name,
        },
    )

    assert response.status_code == 204, response.text

    product = await get_product(
        db_session,
        product_id,
    )

    assert product["nombre"] == new_name
    assert product["slug"] != old_slug
    assert product["base_price"] == Decimal("109.90")


# =========================================================
# 4. ACTUALIZAR MÚLTIPLES CAMPOS
# =========================================================

async def test_update_product_multiple_fields_e2e(
    admin_client: AsyncClient,
    created_product,
    db_session,
):
    product_id = created_product["id"]

    response = await admin_client.patch(
        f"/product/{product_id}",
        data={
            "descripcion": "Descripcion actualizada E2E",
            "fit": "REGULAR",
            "base_price": "159.90",
        },
    )

    assert response.status_code == 204, response.text

    product = await get_product(
        db_session,
        product_id,
    )

    assert product["descripcion"] == (
        "Descripcion actualizada E2E"
    )
    assert product["fit"] == "REGULAR"
    assert product["base_price"] == Decimal("159.90")


# =========================================================
# 5. RECHAZAR PRECIOS INVÁLIDOS
# =========================================================

@pytest.mark.parametrize(
    "price",
    [
        "-10.00",
        "0.00",
        "abc",
    ],
)
async def test_update_product_invalid_price_e2e(
    admin_client: AsyncClient,
    created_product,
    db_session,
    fake_product_cache,
    price,
):
    product_id = created_product["id"]

    response = await admin_client.patch(
        f"/product/{product_id}",
        data={
            "base_price": price,
        },
    )

    assert response.status_code == 422, response.text

    product = await get_product(
        db_session,
        product_id,
    )

    # El precio original debe permanecer intacto.
    assert product["base_price"] == Decimal("109.90")

    # No debería invalidarse Redis.
    assert fake_product_cache["entities"] == []
    assert fake_product_cache["entity"] == []


# =========================================================
# 6. NOMBRE INVÁLIDO
# =========================================================

@pytest.mark.parametrize(
    "nombre",
    [
        "abc",
        "",
        "X" * 56,
    ],
)
async def test_update_product_invalid_name_e2e(
    admin_client: AsyncClient,
    created_product,
    update_product_payload,
    db_session,
    fake_product_cache,
    nombre,
):
    product_id = created_product["id"]

    response = await admin_client.patch(
        f"/product/{product_id}",
        data={
            "nombre": nombre,
        },
    )

    assert response.status_code == 422, response.text

    product = await get_product(
        db_session,
        product_id,
    )

    assert product["nombre"] == (
        update_product_payload["nombre"]
    )

    assert fake_product_cache["entities"] == []
    assert fake_product_cache["entity"] == []


# =========================================================
# 7. PATCH SIN CAMPOS
# =========================================================

async def test_update_product_empty_payload_e2e(
    admin_client: AsyncClient,
    created_product,
    update_product_payload,
    db_session,
):
    product_id = created_product["id"]

    response = await admin_client.patch(
        f"/product/{product_id}",
        data={},
    )

    assert response.status_code == 204, response.text

    product = await get_product(
        db_session,
        product_id,
    )

    assert product["nombre"] == (
        update_product_payload["nombre"]
    )
    assert product["base_price"] == Decimal("109.90")
    assert product["slug"] == created_product["slug"]


# =========================================================
# 8. PRODUCTO INEXISTENTE
# =========================================================

async def test_update_product_not_found_e2e(
    admin_client: AsyncClient,
    fake_product_cache,
):
    product_id = 2147483647

    response = await admin_client.patch(
        f"/product/{product_id}",
        data={
            "base_price": "149.90",
        },
    )

    assert response.status_code == 404, response.text

    assert fake_product_cache["entities"] == []
    assert fake_product_cache["entity"] == []


# =========================================================
# 9. PRODUCTO DESHABILITADO
# =========================================================

async def test_update_disabled_product_e2e(
    admin_client: AsyncClient,
    created_product,
    db_session,
    fake_product_cache,
):
    product_id = created_product["id"]

    # Preparar estado de prueba.
    await db_session.execute(
        text("""
            UPDATE product
            SET is_active = FALSE
            WHERE id = :product_id
        """),
        {"product_id": product_id},
    )
    await db_session.commit()

    response = await admin_client.patch(
        f"/product/{product_id}",
        data={
            "base_price": "149.90",
        },
    )

    # Tu ValidationError de dominio devuelve 400.
    assert response.status_code == 400, response.text

    product = await get_product(
        db_session,
        product_id,
    )

    assert product["base_price"] == Decimal("109.90")
    assert product["is_active"] is False

    assert fake_product_cache["entities"] == []
    assert fake_product_cache["entity"] == []
