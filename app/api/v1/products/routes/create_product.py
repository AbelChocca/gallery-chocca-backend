from app.api.v1.products.product_route import router
from app.api.schemas.products.schema import CreateProductSchema, CreateProductResponse
from app.api.dependencies.products.case_depends import get_create_product_case
from app.api.schemas.products.schema_mapper import InputSchemaMapper
from app.api.security.resolvers.sessions import get_admin_session
from app.api.schemas.products.types import ProductImageType

from app.application.products.cases.create_product import CreateProductUseCase

from fastapi import status, Depends, File, Form 
from typing import Annotated
import orjson

@router.post(
    "/publish/",
    response_model=CreateProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create an product"
)
async def create_product(
    product_schema_json: Annotated[str, Form(...)],
    files: Annotated[ProductImageType, File(...)],
    case: Annotated[CreateProductUseCase, Depends(get_create_product_case)],
    _: Annotated[None, Depends(get_admin_session)]
) -> CreateProductResponse:
    data = orjson.loads(product_schema_json)   
    schema: CreateProductSchema = CreateProductSchema(**data)
    res = await case.execute(
        [file.file for file in files],
        InputSchemaMapper.to_publish_command(schema)
        )
    return CreateProductResponse(id=res.id,slug=res.slug)