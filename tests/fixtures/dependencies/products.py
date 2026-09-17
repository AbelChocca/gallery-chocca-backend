import pytest_asyncio
from decimal import Decimal

from app.features.products.models.model_product import VariantSizeTable, ProductTable, VariantTable
from app.features.inventory.models.inventory_location import InventoryLocationTable
from app.features.inventory.types.inventory_location import InventoryLocationType

from app.features.products.types import (
    BrandType,
    CategoryType,
    FitType,
)

@pytest_asyncio.fixture
async def catalog_short_product(db_session):
    short = ProductTable(
        nombre="Short Catalog Test",
        descripcion="Short para pruebas de pricing en catálogo",
        brand=BrandType.BGOO,
        category=CategoryType.SHORT,
        fit=FitType.REGULAR,
        slug="catalog-short-test",
        base_price=Decimal("80.00"),
    )

    db_session.add(short)
    await db_session.commit()
    await db_session.refresh(short)

    return short

@pytest_asyncio.fixture
async def pricing_products(db_session):
    products = [
        ProductTable(
            nombre="Polo Pricing Test",
            descripcion="Producto para pruebas del motor de pricing",
            brand=BrandType.BGOO,
            category=CategoryType.PANT,
            fit=FitType.REGULAR,
            slug="pricing-polo-test",
            base_price=Decimal("50.00"),
        ),
        ProductTable(
            nombre="Jean Pricing Test",
            descripcion="Producto para pruebas del motor de pricing",
            brand=BrandType.BGOO,
            category=CategoryType.PANT,
            fit=FitType.REGULAR,
            slug="pricing-jean-test",
            base_price=Decimal("100.00"),
        ),
        ProductTable(
            nombre="Casaca Pricing Test",
            descripcion="Producto para pruebas del motor de pricing",
            brand=BrandType.BGOO,
            category=CategoryType.PANT,
            fit=FitType.REGULAR,
            slug="pricing-casaca-test",
            base_price=Decimal("150.00"),
        ),
    ]

    db_session.add_all(products)
    await db_session.commit()

    for product in products:
        await db_session.refresh(product)

    variants = [
        VariantTable(
            product_id=products[0].id,
            color="Negro",
        ),
        VariantTable(
            product_id=products[0].id,
            color="Blanco",
        ),
        VariantTable(
            product_id=products[1].id,
            color="Azul",
        ),
        VariantTable(
            product_id=products[1].id,
            color="Negro",
        ),
        VariantTable(
            product_id=products[2].id,
            color="Negro",
        ),
        VariantTable(
            product_id=products[2].id,
            color="Beige",
        ),
    ]

    db_session.add_all(variants)
    await db_session.commit()

    for variant in variants:
        await db_session.refresh(variant)

    variant_sizes = [
        VariantSizeTable(
            variant_id=variants[0].id,
            size="M",
            sku="PRICING-POLO-NEGRO-M",
            barcode="PRICING-BARCODE-001",
        ),
        VariantSizeTable(
            variant_id=variants[1].id,
            size="M",
            sku="PRICING-POLO-BLANCO-M",
            barcode="PRICING-BARCODE-002",
        ),
        VariantSizeTable(
            variant_id=variants[2].id,
            size="M",
            sku="PRICING-JEAN-AZUL-M",
            barcode="PRICING-BARCODE-003",
        ),
        VariantSizeTable(
            variant_id=variants[3].id,
            size="M",
            sku="PRICING-JEAN-NEGRO-M",
            barcode="PRICING-BARCODE-004",
        ),
        VariantSizeTable(
            variant_id=variants[4].id,
            size="M",
            sku="PRICING-CASACA-NEGRO-M",
            barcode="PRICING-BARCODE-005",
        ),
        VariantSizeTable(
            variant_id=variants[5].id,
            size="M",
            sku="PRICING-CASACA-BEIGE-M",
            barcode="PRICING-BARCODE-006",
        ),
    ]

    db_session.add_all(variant_sizes)
    await db_session.commit()

    for variant_size in variant_sizes:
        await db_session.refresh(variant_size)

    return {
        "products": products,
        "variants": variants,
        "variant_sizes": variant_sizes,
    }


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