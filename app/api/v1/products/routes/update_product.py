from app.api.v1.products.product_route import router
from app.api.schemas.products.schema import UpdateProductSchema
from app.api.schemas.products.schema_mapper import InputSchemaMapper
from app.application.products.cases.update_product import UpdateProductCase
from app.api.dependencies.products.case_depends import get_update_product_case
from app.api.security.resolvers.sessions import get_admin_session
from app.api.schemas.products.types import ProductImageType

from fastapi import status, Depends, File, Form, Path
from typing import Annotated
import orjson

@router.patch(
    "/update/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update an product"
)
async def update_product(
    product_id: Annotated[int, Path(...)],
    update_json: Annotated[str, Form(...)],
    case: Annotated[UpdateProductCase, Depends(get_update_product_case)],
    _: Annotated[None, Depends(get_admin_session)],
    files: ProductImageType = File([])
) -> None:
    data = orjson.loads(update_json)
    update_schema: UpdateProductSchema = UpdateProductSchema(**data)
    new_images = [file.file for file in files] if files else None
    await case.execute(
        InputSchemaMapper.to_update_command(update_schema),
        product_id,
        new_images
        )