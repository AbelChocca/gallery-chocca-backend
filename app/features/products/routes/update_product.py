from app.features.products.product_route import router
from app.features.products.schema import UpdateProductSchema
from app.features.products.schema_mapper import InputSchemaMapper
from app.api.security.resolvers.sessions import get_admin_session
from app.features.products.types import ProductImageType
from app.features.products.service import ProductService
from app.features.products.dependency import get_product_service

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
    service: Annotated[ProductService, Depends(get_product_service)],
    _: Annotated[None, Depends(get_admin_session)],
    files: ProductImageType = File([])
) -> None:
    data = orjson.loads(update_json)
    update_schema: UpdateProductSchema = UpdateProductSchema(**data)
    new_images = [file.file for file in files] if files else None
    await service.update_product_with_variants(
        command=InputSchemaMapper.to_update_command(update_schema),
        product_id=product_id,
        new_images_file=new_images
        )