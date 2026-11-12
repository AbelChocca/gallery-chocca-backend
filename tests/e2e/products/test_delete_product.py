
import io
import json
from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy import text

from app.features.products.schema import (
    CategoryType,
    BrandType,
    SizeType,
)
from app.features.media.service import MediaService


pytestmark = pytest.mark.asyncio(
    loop_scope="session",
)

def unique_letters() -> str:
    value = uuid4().int
    letters = []

    for _ in range(12):
        value, remainder = divmod(value, 26)
        letters.append(chr(ord("a") + remainder))

    return "".join(letters)


@pytest.fixture
def delete_product_payload(location):
    unique = unique_letters()

    return {
        "nombre": f"Jean Prueba {unique}",
        "descripcion": "Producto para pruebas de eliminación",
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
    delete_product_payload,
    fake_product_media,
    fake_product_media_delete,
    fake_product_cache,
):
    response = await admin_client.post(
        "/product/publish/",
        data={
            "product_schema_json": json.dumps(
                delete_product_payload
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

    fake_product_cache["entities"].clear()
    fake_product_cache["entity"].clear()

    return response.json()


async def product_exists(
    db_session,
    product_id: int,
) -> bool:
    result = await db_session.execute(
        text("""
            SELECT EXISTS (
                SELECT 1
                FROM product
                WHERE id = :product_id
            )
        """),
        {"product_id": product_id},
    )

    return result.scalar_one()


# =========================================================
# 1. ELIMINACIÓN EXITOSA
# =========================================================

async def test_delete_product_success_e2e(
    admin_client: AsyncClient,
    created_product,
    db_session,
    fake_product_cache,
    fake_product_media_delete,
):
    product_id = created_product["id"]

    assert await product_exists(db_session, product_id)

    response = await admin_client.delete(
        f"/product/delete/{product_id}"
    )

    assert response.status_code == 200, response.text

    assert response.json() == {
        "message": "Product was deleted successfully"
    }

    # Se espera eliminación física.
    assert not await product_exists(
        db_session,
        product_id,
    )

    assert fake_product_cache["entity"] == [
        ("product", product_id)
    ]

    assert fake_product_cache["entities"] == [
        "product"
    ]

    assert len(
        fake_product_media_delete["delete_images"]
    ) == 1

    assert (
        fake_product_media_delete["delete_images"][0][
            "owner_type"
        ] == "variant"
    )

    assert len(
        fake_product_media_delete["move_images_to_trash"]
    ) == 1


# =========================================================
# 2. PRODUCTO INEXISTENTE
# =========================================================

async def test_delete_product_not_found_e2e(
    admin_client: AsyncClient,
    fake_product_cache,
    fake_product_media_delete,
):
    product_id = 2147483647

    response = await admin_client.delete(
        f"/product/delete/{product_id}"
    )

    assert response.status_code == 404, response.text

    assert fake_product_cache["entities"] == []
    assert fake_product_cache["entity"] == []

    assert (
        fake_product_media_delete["delete_images"]
        == []
    )

    assert (
        fake_product_media_delete["move_images_to_trash"]
        == []
    )

async def test_delete_product_unauthenticated_e2e(
    http_client: AsyncClient,
    created_product,
    db_session,
    fake_product_cache,
    fake_product_media_delete,
):
    product_id = created_product["id"]

    http_client.cookies.clear()

    response = await http_client.delete(
        f"/product/delete/{product_id}"
    )

    assert response.status_code in (
        401,
        403,
    ), response.text

    assert await product_exists(
        db_session,
        product_id,
    )

    assert fake_product_cache["entities"] == []
    assert fake_product_cache["entity"] == []

    assert (
        fake_product_media_delete["delete_images"]
        == []
    )


async def test_delete_product_media_failure_rollback_e2e(
    admin_client: AsyncClient,
    created_product,
    db_session,
    fake_product_cache,
    monkeypatch,
):
    product_id = created_product["id"]

    assert await product_exists(
        db_session,
        product_id,
    )

    async def failing_move_images_to_trash(
        self,
        *,
        images_public_id,
    ):
        raise RuntimeError(
            "Simulated external storage failure"
        )

    monkeypatch.setattr(
        MediaService,
        "move_images_to_trash",
        failing_move_images_to_trash,
    )

    response = await admin_client.delete(
        f"/product/delete/{product_id}"
    )

    assert response.status_code == 500, response.text

    assert await product_exists(
        db_session,
        product_id,
    )

    assert fake_product_cache["entities"] == []
    assert fake_product_cache["entity"] == []
