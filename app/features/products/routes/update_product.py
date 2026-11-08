
from fastapi import Depends, Form, Path, status
from typing import Annotated

from app.features.products.schema import UpdateProductSchema
from app.features.products.dependency import get_update_product_use_case
from app.features.products.use_cases.update_product import (
    UpdateProductUseCase,
)
from app.core.authorization.dependencies import require_permission, Permission
from app.features.products.product_route import router


@router.patch(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update a product",
    dependencies=[
        require_permission(Permission.PRODUCT_UPDATE)
    ],
)
async def update_product(
    product_id: Annotated[int, Path(gt=0)],
    update_schema: Annotated[UpdateProductSchema, Form()],
    use_case: Annotated[
        UpdateProductUseCase,
        Depends(get_update_product_use_case),
    ],
) -> None:
    await use_case.execute(
        product_id=product_id,
        nombre=update_schema.nombre,
        descripcion=update_schema.descripcion,
        brand=update_schema.brand,
        category=update_schema.category,
        fit=update_schema.fit,
        base_price=update_schema.base_price,
    )