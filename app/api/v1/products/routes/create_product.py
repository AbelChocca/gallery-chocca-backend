from app.api.v1.products.product_route import router
from app.api.schemas.products.schema import ProductRead, CreateProductSchema
from app.api.dependencies.products.case_depends import get_create_product_case
from app.api.schemas.products.schema_mapper import InputSchemaMapper, OutputSchemaMapper
from app.api.security.dependencies.sessions import get_auth_sessions, SecuritySessions

from app.application.products.cases.create_product import CreateProductUseCase

from fastapi import status, Depends, UploadFile, File
from typing import List

@router.post(
    "/publish/",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create an product"
)
async def create_product(
    schema: CreateProductSchema,
    files: List[UploadFile] = File(...),
    case: CreateProductUseCase = Depends(get_create_product_case),
    admin_auth: SecuritySessions = Depends(get_auth_sessions)
) -> ProductRead:
    await admin_auth.get_admin()
    res = await case.execute(
        images_file=[file.file for file in files],
        command=InputSchemaMapper.to_publish_command(schema)
        )
    return OutputSchemaMapper.to_read_schema(dto=res)