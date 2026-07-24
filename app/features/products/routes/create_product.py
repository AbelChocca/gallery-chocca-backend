from app.features.products.product_route import router
from app.features.products.schema import (
    CreateProductSchema,
    CreateProductResponse,
)
from app.features.products.mappers.schema_mapper import (
    InputSchemaMapper,
)
from app.features.products.types import ProductImageType

from app.features.products.dependency import (
    get_create_product_use_case,
)
from app.features.products.use_cases.create_product import (
    CreateProductUseCase,
)

from app.core.authorization.dependencies import (
    require_permission,
)
from app.api.security.resolvers.sessions import get_user_id
from app.core.authorization.permissions import Permission

from fastapi import (
    status,
    Depends,
    File,
    Form,
)

from typing import Annotated

import orjson


@router.post(
    "/publish/",
    response_model=CreateProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a product",
    dependencies=[
        require_permission(Permission.PRODUCT_CREATE),
    ],
)
async def create_product(
    product_schema_json: Annotated[str, Form(...)],
    files: Annotated[ProductImageType, File(...)],
    user_id: Annotated[int, Depends(get_user_id)],
    use_case: Annotated[
        CreateProductUseCase,
        Depends(get_create_product_use_case),
    ],
) -> CreateProductResponse:

    data = orjson.loads(product_schema_json)

    schema = CreateProductSchema(**data)

    response = await use_case.execute(
        images_file=[file.file for file in files],
        command=InputSchemaMapper.to_publish_command(schema),
        user_id=user_id,
    )

    return CreateProductResponse.model_validate(response)