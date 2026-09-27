from datetime import datetime, timezone
from decimal import Decimal

import pytest

pytestmark = pytest.mark.asyncio(
    loop_scope="session",
)


from app.features.sales.types.sale import SaleChannel
from app.features.products.types import CategoryType
from app.features.sales.types.customer import CustomerType
from tests.helpers.create_test_promotion import create_category_target_promotion, create_category_audience_promotion, create_catalog_condition_promotion
from app.features.pricing.dtos.catalog_pricing_dto import CatalogPricingContext, CatalogPricingItemDTO
from app.features.pricing.types.promotion_types import PromotionAudienceType, PromotionConditionType
from app.features.products.types import CategoryType, BrandType, FitType
from app.features.products.models.model_product import ProductTable


async def test_catalog_pricing_applies_public_pant_promotion_only_to_pants(
    db_session,
    catalog_pricing_service,
    pricing_products,
    catalog_short_product,
):
    products = pricing_products["products"]

    pant = products[0]
    short = catalog_short_product["product"]

    await create_category_target_promotion(
        db_session,
        category=CategoryType.PANT,
        discount="10",
    )

    context = CatalogPricingContext(
        items=[
            CatalogPricingItemDTO(
                product_id=pant.id,
                category=pant.category,
                brand=pant.brand,
                unit_price=pant.base_price,
            ),
            CatalogPricingItemDTO(
                product_id=short.id,
                category=short.category,
                brand=short.brand,
                unit_price=short.base_price,
            ),
        ],
        sale_channel=SaleChannel.ECOMMERCE,
        customer_id=None,
        customer_type=None,
        now=datetime.now(timezone.utc),
    )

    result = await catalog_pricing_service.calculate(
        context=context,
    )

    pant_result = next(
        item for item in result
        if item.product_id == pant.id
    )

    short_result = next(
        item for item in result
        if item.product_id == short.id
    )

    assert pant_result.final_price == Decimal("45.00")
    assert pant_result.discount_amount == Decimal("5.00")

    assert short_result.final_price == Decimal("80.00")
    assert short_result.discount_amount == Decimal("0.00")


async def test_catalog_pricing_respects_customer_audience(
    db_session,
    catalog_pricing_service,
    pricing_products,
    pricing_customer,
):
    pant = pricing_products["products"][0]
    customer = pricing_customer

    await create_category_audience_promotion(
        db_session,
        category=CategoryType.PANT,
        audience_type=PromotionAudienceType.CUSTOMER,
        reference_id=customer.id,
        discount="10",
    )

    def build_context(
        *,
        customer_id: int | None,
        customer_type: CustomerType | None,
    ):
        return CatalogPricingContext(
            items=[
                CatalogPricingItemDTO(
                    product_id=pant.id,
                    category=pant.category,
                    brand=pant.brand,
                    unit_price=pant.base_price,
                )
            ],
            sale_channel=SaleChannel.ECOMMERCE,
            customer_id=customer_id,
            customer_type=customer_type,
            now=datetime.now(timezone.utc),
        )

    # Customer dentro de la audiencia
    result = await catalog_pricing_service.calculate(
        context=build_context(
            customer_id=customer.id,
            customer_type=customer.customer_type,
        )
    )

    assert result[0].final_price == Decimal("45.00")

    # Anónimo
    result = await catalog_pricing_service.calculate(
        context=build_context(
            customer_id=None,
            customer_type=None,
        )
    )

    assert result[0].final_price == Decimal("50.00")

    # Otro cliente
    result = await catalog_pricing_service.calculate(
        context=build_context(
            customer_id=999999,
            customer_type=CustomerType.REGULAR,
        )
    )

    assert result[0].final_price == Decimal("50.00")


@pytest.mark.parametrize(
    ("condition_type", "parameters"),
    [
        (
            PromotionConditionType.PAYMENT_METHOD,
            {"payment_method": "YAPE"},
        ),
        (
            PromotionConditionType.MINIMUM_ORDER_AMOUNT,
            {"minimum_amount": "100.00"},
        ),
        (
            PromotionConditionType.MINIMUM_PRODUCT_QUANTITY,
            {"minimum_quantity": 2},
        ),
    ],
)
async def test_catalog_does_not_preview_promotions_requiring_missing_context(
    db_session,
    catalog_pricing_service,
    pricing_products,
    condition_type,
    parameters,
):
    pant = pricing_products["products"][0]

    await create_catalog_condition_promotion(
        db_session,
        category=CategoryType.PANT,
        condition_type=condition_type,
        parameters=parameters,
    )

    context = CatalogPricingContext(
        items=[
            CatalogPricingItemDTO(
                product_id=pant.id,
                category=pant.category,
                brand=pant.brand,
                unit_price=pant.base_price,
            )
        ],
        sale_channel=SaleChannel.ECOMMERCE,
        customer_id=None,
        customer_type=None,
        now=datetime.now(timezone.utc),
    )

    result = await catalog_pricing_service.calculate(
        context=context,
    )

    assert result[0].final_price == Decimal("50.00")
    assert result[0].discount_amount == Decimal("0.00")


async def test_catalog_pricing_calculates_multiple_products_in_batch(
    db_session,
    catalog_pricing_service,
):
    products = []

    categories = (
        [CategoryType.PANT] * 10
        + [CategoryType.SHORT] * 5
        + [CategoryType.SHIRT] * 5
    )

    for index, category in enumerate(categories):
        product = ProductTable(
            nombre=f"Catalog Batch Product {index}",
            descripcion="Producto para test batch",
            brand=BrandType.BGOO,
            category=category,
            fit=FitType.REGULAR,
            slug=f"catalog-batch-product-{index}",
            base_price=Decimal("100.00"),
        )

        products.append(product)

    db_session.add_all(products)
    await db_session.commit()

    for product in products:
        await db_session.refresh(product)

    await create_category_target_promotion(
        db_session,
        category=CategoryType.PANT,
        discount="10",
    )

    context = CatalogPricingContext(
        items=[
            CatalogPricingItemDTO(
                product_id=product.id,
                category=product.category,
                brand=product.brand,
                unit_price=product.base_price,
            )
            for product in products
        ],
        sale_channel=SaleChannel.ECOMMERCE,
        customer_id=None,
        customer_type=None,
        now=datetime.now(timezone.utc),
    )

    result = await catalog_pricing_service.calculate(
        context=context,
    )

    assert len(result) == 20

    results_by_product = {
        item.product_id: item
        for item in result
    }

    for product in products:
        priced = results_by_product[product.id]

        if product.category == CategoryType.PANT:
            assert priced.final_price == Decimal("90.00")
            assert priced.discount_amount == Decimal("10.00")
        else:
            assert priced.final_price == Decimal("100.00")
            assert priced.discount_amount == Decimal("0.00")