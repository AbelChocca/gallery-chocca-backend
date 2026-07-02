from app.features.products.product_route import router
from app.features.products.schema import UpdateProductSchema
from app.features.products.schema_mapper import InputSchemaMapper
from app.features.products.types import ProductImageType
from app.features.products.service import ProductService
from app.features.products.dependency import get_product_service
from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission

from fastapi import status, Depends, File, Form, Path
from typing import Annotated
import orjson

@router.patch(
    "/update/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update an product",
    dependencies=[
        require_permission(Permission.PRODUCT_UPDATE)
    ]
)
async def update_product(
    product_id: Annotated[int, Path(...)],
    update_json: Annotated[str, Form(...)],
    service: Annotated[ProductService, Depends(get_product_service)],
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