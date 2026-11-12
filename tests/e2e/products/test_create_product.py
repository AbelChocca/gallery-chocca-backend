
import io
import json
from copy import deepcopy
from uuid import uuid4
from decimal import Decimal

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


def unique_letters() -> str:
    value = uuid4().int
    letters = []

    for _ in range(12):
        value, remainder = divmod(value, 26)
        letters.append(chr(ord("a") + remainder))

    return "".join(letters)

@pytest.fixture
def product_payload(location):
    unique = unique_letters()

    return {
        "nombre": f"Jean Prueba {unique}",
        "descripcion": "Producto de prueba automatizada",
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
                        "barcode": f"E2E-{unique}",
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


async def publish_product(
    client: AsyncClient,
    payload: dict,
    *,
    image_count: int = 1,
):
    files = [
        (
            "files",
            (
                f"product-{index}.jpg",
                io.BytesIO(b"fake-image-content"),
                "image/jpeg",
            ),
        )
        for index in range(image_count)
    ]

    return await client.post(
        "/product/publish/",
        data={
            "product_schema_json": json.dumps(payload),
        },
        files=files,
    )


async def test_create_product_success_e2e(
    admin_client: AsyncClient,
    db_session,
    product_payload,
    fake_product_media,
    fake_product_cache,
):
    response = await publish_product(
        admin_client,
        product_payload,
    )

    assert response.status_code == 201, response.text

    data = response.json()

    assert isinstance(data["id"], int)
    assert data["id"] > 0
    assert isinstance(data["slug"], str)
    assert data["slug"]

    # Ajustar al nombre real de tu tabla de productos.
    result = await db_session.execute(
        text("""
            SELECT id, nombre, slug, base_price
            FROM product
            WHERE id = :product_id
        """),
        {"product_id": data["id"]},
    )

    product = result.mappings().one_or_none()

    assert product is not None
    assert product["nombre"] == product_payload["nombre"]
    assert product["slug"] == data["slug"]
    assert product["base_price"] == Decimal("109.90")

    # Verificar interacción simulada con Cloudinary.
    assert len(fake_product_media.uploads) == 1
    assert len(fake_product_media.batches) == 1

    batch = fake_product_media.batches[0]
    assert batch["owner_id"] > 0
    assert len(batch["uploads"]) == 1

    # Verificar solicitud de invalidación de Redis.
    assert len(fake_product_cache["entities"]) == 1

async def test_create_product_multiple_variants_e2e(
    admin_client: AsyncClient,
    product_payload,
    fake_product_media,
    fake_product_cache,
):
    payload = deepcopy(product_payload)

    payload["variants"].append({
        "color": "navy",
        "temp_key": "variant-navy",
        "sizes": [
            {
                "size": payload["variants"][0]["sizes"][0]["size"],
                "barcode": None,
                "inventories": [],
            }
        ],
    })

    payload["temp_keys"] = [
        "variant-black",
        "variant-navy",
    ]

    response = await publish_product(
        admin_client,
        payload,
        image_count=2,
    )

    assert response.status_code == 201, response.text

    data = response.json()

    assert data["id"] > 0
    assert len(fake_product_media.uploads) == 2
    assert len(fake_product_media.batches) == 2

    owner_ids = {
        batch["owner_id"]
        for batch in fake_product_media.batches
    }

    assert len(owner_ids) == 2

    for batch in fake_product_media.batches:
        assert len(batch["uploads"]) == 1

    assert len(fake_product_cache["entities"]) == 1


@pytest.mark.parametrize(
    "changes",
    [
        {"nombre": ""},
        {"nombre": "A"},
        {"nombre": "X" * 256},
        {"variants": []},
        {"base_price": "-1.00"},
        {"base_price": "abc"},
        {"base_price": None},
    ],
)
async def test_create_product_invalid_payload_e2e(
    admin_client: AsyncClient,
    product_payload,
    fake_product_media,
    fake_product_cache,
    changes,
):
    payload = {
        **product_payload,
        **changes,
    }

    response = await publish_product(
        admin_client,
        payload,
    )

    assert response.status_code == 400, response.text

    assert fake_product_media.uploads == []
    assert fake_product_cache == {
    "entities": [],
    "entity": [],
}


async def test_create_product_image_count_mismatch_e2e(
    admin_client: AsyncClient,
    product_payload,
    fake_product_media,
    fake_product_cache,
):
    payload = deepcopy(product_payload)

    # 2 temp_keys, pero solamente 1 archivo.
    payload["temp_keys"] = [
        "variant-black",
        "variant-black",
    ]

    response = await publish_product(
        admin_client,
        payload,
        image_count=1,
    )

    assert response.status_code in (400, 422), response.text

    assert fake_product_media.uploads == []
    assert fake_product_cache == {
    "entities": [],
    "entity": [],
}


async def test_create_product_unknown_image_key_e2e(
    admin_client: AsyncClient,
    db_session,
    product_payload,
    fake_product_media,
    fake_product_cache,
):
    payload = deepcopy(product_payload)

    payload["temp_keys"] = [
        "variant-inexistente",
    ]

    response = await publish_product(
        admin_client,
        payload,
    )

    assert response.status_code in (400, 422), response.text

    # La Saga debe revertir toda la creación.
    result = await db_session.execute(
        text("""
            SELECT COUNT(*)
            FROM product
            WHERE nombre = :nombre
        """),
        {"nombre": payload["nombre"]},
    )

    assert result.scalar_one() == 0

    assert fake_product_media.uploads == []
    assert fake_product_cache == {
    "entities": [],
    "entity": [],
}


async def test_create_product_unauthenticated_e2e(
    http_client: AsyncClient,
    product_payload,
    fake_product_media,
    fake_product_cache,
):
    http_client.cookies.clear()

    response = await publish_product(
        http_client,
        product_payload,
    )

    assert response.status_code in (401, 403), response.text

    assert fake_product_media.uploads == []
    assert fake_product_cache == {
    "entities": [],
    "entity": [],
}
