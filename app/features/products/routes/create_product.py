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
    UploadFile
)

from typing import Annotated

from pydantic import ValidationError as PydanticValidationError
from app.core.exceptions import ValidationError

import orjson

MAX_IMAGES = 40
MAX_IMAGE_SIZE = 5 * 1024 * 1024


def validate_product_images(
    files: list[UploadFile],
) -> None:
    if not 1 <= len(files) <= MAX_IMAGES:
        raise ValidationError(
            message="Debes enviar entre 1 y 40 imágenes.",
            context={"field": "files"},
        )

    for index, file in enumerate(files):
        stream = file.file

        stream.seek(0, 2)
        size = stream.tell()
        stream.seek(0)

        if size == 0 or size > MAX_IMAGE_SIZE:
            raise ValidationError(
                message="La imagen debe pesar entre 1 byte y 5 MB.",
                context={
                    "field": "files",
                    "index": index,
                    "size": size,
                },
            )

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

    
    try:
        data = orjson.loads(product_schema_json)
        schema = CreateProductSchema.model_validate(data)

    except orjson.JSONDecodeError as exc:
        raise ValidationError(
            message="El JSON del producto tiene un formato inválido.",
            context={
                "field": "product_schema_json",
                "error": "invalid_json",
            },
        ) from exc

    except PydanticValidationError as exc:
        raise ValidationError(
            message="Los datos del producto no son válidos.",
            context={
                "field": "product_schema_json",
                "errors": exc.errors(
                    include_url=False,
                    include_context=False,
                    include_input=False,
                ),
            },
        ) from exc

    validate_product_images(files)

    response = await use_case.execute(
        images_file=[file.file for file in files],
        command=InputSchemaMapper.to_publish_command(schema),
        user_id=user_id,
    )

    return CreateProductResponse.model_validate(response)