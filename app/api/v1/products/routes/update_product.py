from app.api.v1.products.product_route import router
from app.api.schemas.products.schema import ProductRead, UpdateProductSchema
from app.api.schemas.products.schema_mapper import InputSchemaMapper, OutputSchemaMapper
from app.application.products.cases.update_product import UpdateProductCase
from app.api.dependencies.products.case_depends import get_update_product_case
from app.api.security.dependencies.sessions import get_auth_sessions, SecuritySessions

from fastapi import status, Depends, UploadFile, File
from typing import List, Optional

@router.patch(
    "/update/{product_id}",
    response_model=ProductRead,
    status_code=status.HTTP_200_OK,
    summary="Update an product"
)
async def update_product(
    product_id: int,
    update_schema: UpdateProductSchema,
    files: Optional[List[UploadFile]] = File(None),
    case: UpdateProductCase = Depends(get_update_product_case),
    auth_session: SecuritySessions = Depends(get_auth_sessions)
) -> UpdateProductSchema:
    await auth_session.get_admin()
    command = InputSchemaMapper.to_update_command(update_schema)
    res = await case.execute(
        command=command,
        product_id=product_id,
        new_images_file=[file.file for file in files]
        )
    return OutputSchemaMapper.to_read_schema(res)