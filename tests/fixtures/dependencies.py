import pytest_asyncio
from app.features.products.models.model_product import VariantSizeTable, ProductTable, VariantTable
from app.features.inventory.models.inventory_location import InventoryLocationTable
from app.features.inventory.types.inventory_location import InventoryLocationType

from app.features.products.types import (
    BrandType,
    CategoryType,
    FitType,
)


@pytest_asyncio.fixture
async def product(db_session):

    product = ProductTable(
        nombre="Polo Test",
        descripcion="Producto para pruebas",
        brand=BrandType.BGOO,
        category=CategoryType.PANT,
        fit=FitType.REGULAR,
        slug="polo-test",
    )

    db_session.add(product)

    await db_session.commit()
    await db_session.refresh(product)

    return product

@pytest_asyncio.fixture
async def variant(
    db_session,
    product,
):

    variant = VariantTable(
        product_id=product.id,
        color="Negro",
    )

    db_session.add(variant)

    await db_session.commit()
    await db_session.refresh(variant)

    return variant


@pytest_asyncio.fixture
async def variant_size(
    db_session,
    variant,
):
    variant_size = VariantSizeTable(
        variant_id=variant.id,
        size="M",
        sku="TEST-M",
        barcode="TEST-BARCODE-M",
    )

    db_session.add(variant_size)

    await db_session.commit()
    await db_session.refresh(variant_size)

    return variant_size

@pytest_asyncio.fixture
async def location(db_session):
    location = InventoryLocationTable(
        name="Test Store",
        type=InventoryLocationType.STORE,
        address="Gamarra, jr. atahualpa. Lima, Peru."
    )

    db_session.add(location)
    await db_session.commit()

    await db_session.refresh(location)

    return location