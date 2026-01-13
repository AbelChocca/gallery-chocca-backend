from app.api.v1.products.product_route import router
from app.api.schemas.products.schema import ProductRead, CreateProductSchema
from app.api.dependencies.products.case_depends import get_create_product_case
from app.api.schemas.products.schema_mapper import InputSchemaMapper, OutputSchemaMapper
from app.api.security.dependencies.sessions import get_admin_session

from app.application.products.cases.create_product import CreateProductUseCase

from fastapi import status, Depends, UploadFile, File, Form
from fastapi.concurrency import run_in_threadpool
from json import loads
from typing import List, Annotated

@router.post(
    "/publish/",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create an product"
)
async def create_product(
    product_schema_json: Annotated[str, Form(...)],
    files: Annotated[List[UploadFile], File(...)],
    case: Annotated[CreateProductUseCase, Depends(get_create_product_case)],
    _: Annotated[None, Depends(get_admin_session)]
) -> ProductRead:
    data = loads(product_schema_json)   
    schema: CreateProductSchema = CreateProductSchema(**data)
    res = await run_in_threadpool(case.execute,
        [file.file for file in files],
        InputSchemaMapper.to_publish_command(schema)
        )
    return OutputSchemaMapper.to_read_schema(dto=res)