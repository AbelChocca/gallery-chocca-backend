from app.api.v1.products.product_route import router
from app.api.schemas.products.schema import ProductRead, UpdateProductSchema
from app.api.schemas.products.schema_mapper import InputSchemaMapper, OutputSchemaMapper
from app.application.products.cases.update_product import UpdateProductCase
from app.api.dependencies.products.case_depends import get_update_product_case
from app.api.security.dependencies.sessions import get_auth_sessions, SecuritySessions

from fastapi import status, Depends, UploadFile, File, Form, Path
from typing import List, Optional, Annotated
from json import loads

@router.patch(
    "/update/{product_id}",
    response_model=ProductRead,
    status_code=status.HTTP_200_OK,
    summary="Update an product"
)
async def update_product(
    product_id: Annotated[int, Path(...)],
    update_json: Annotated[str, Form(...)],
    case: Annotated[UpdateProductCase, Depends(get_update_product_case)],
    auth_session: Annotated[SecuritySessions, Depends(get_auth_sessions)],
    files: Annotated[Optional[List[UploadFile]], File()] = None
) -> ProductRead:
    await auth_session.get_admin()
    data = loads(update_json)
    update_schema: UpdateProductSchema = UpdateProductSchema(**data)
    new_images = [file.file for file in files] if files else None
    res = await case.execute(
        command=InputSchemaMapper.to_update_command(update_schema),
        product_id=product_id,
        new_images_file=new_images
        )
    return OutputSchemaMapper.to_read_schema(res)