from app.features.products.product_route import router
from app.features.products.schema import CreateProductSchema, CreateProductResponse
from app.features.products.schema_mapper import InputSchemaMapper
from app.features.products.types import ProductImageType
from app.features.products.service import ProductService
from app.features.products.dependency import get_product_service
from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission

from fastapi import status, Depends, File, Form 
from typing import Annotated
import orjson

@router.post(
    "/publish/",
    response_model=CreateProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create an product",
    dependencies=[
        require_permission(Permission.PRODUCT_CREATE)
    ]
)
async def create_product(
    product_schema_json: Annotated[str, Form(...)],
    files: Annotated[ProductImageType, File(...)],
    service: Annotated[ProductService, Depends(get_product_service)]
) -> CreateProductResponse:
    data = orjson.loads(product_schema_json)   
    schema: CreateProductSchema = CreateProductSchema(**data)
    res = await service.create_product_with_variants(
        [file.file for file in files],
        InputSchemaMapper.to_publish_command(schema)
        )
    return CreateProductResponse(**res)