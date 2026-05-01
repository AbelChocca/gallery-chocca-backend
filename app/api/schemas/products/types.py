from app.api.schemas.validator_helpers import max_length_validator, max_file_size_validator
from typing import Annotated, List
from fastapi import UploadFile, Query
from pydantic import WrapValidator
from app.api.schemas.products.schema import FilterSchema
from app.domain.product.dto.product_dto import BrandType, CategoryType, ColorFilter


ProductImageType = Annotated[
    List[UploadFile],
    WrapValidator(
        max_length_validator(40),
        max_file_size_validator(5 * 1024 * 1024)
    )
]

def filter_dep(
    name: str | None = Query(None),
    marca: BrandType | None = Query(None),
    categoria: CategoryType | None = Query(None),
    model_family: str | None = Query(None),
    color: ColorFilter | None = Query(None),
    sizes: List[str] | None = Query(None),
    sku: str | None = Query(None),
) -> FilterSchema:
    return FilterSchema(
        name=name,
        marca=marca,
        categoria=categoria,
        model_family=model_family,
        color=color,
        sizes=sizes,
        sku=sku
    )