from app.features.products.product_route import router
from app.features.products.schema import UpdateProductSchema
from app.features.products.mappers.schema_mapper import InputSchemaMapper
from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission
from app.features.products.dependency import get_update_product_use_case
from app.features.products.use_cases.update_product import UpdateProductUseCase

from fastapi import status, Depends, Form, Path
from typing import Annotated

@router.patch(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update an product",
    dependencies=[
        require_permission(Permission.PRODUCT_UPDATE)
    ]
)
async def update_product(
    product_id: Annotated[int, Path(...)],
    update_schema: Annotated[UpdateProductSchema, Form(...)],
    use_case: Annotated[UpdateProductUseCase, Depends(get_update_product_use_case)],
) -> None:
    
    await use_case.execute(
        command=InputSchemaMapper.to_update_command(update_schema),
        product_id=product_id,
        )