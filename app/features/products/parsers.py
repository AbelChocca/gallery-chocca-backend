from fastapi import Query
from app.features.products.schema import FilterSchema
from app.features.products.types import BrandType, CategoryType, ColorFilter

def filter_dep(
    name: str | None = Query(None),
    marca: BrandType | None = Query(None),
    categoria: CategoryType | None = Query(None),
    color: ColorFilter | None = Query(None),
    sizes: list[str] | None = Query(None),
    sku: str | None = Query(None),
) -> FilterSchema:
    return FilterSchema(
        name=name,
        brand=marca,
        category=categoria,
        color=color,
        sizes=sizes,
        sku=sku
    )