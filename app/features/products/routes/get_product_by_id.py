from app.features.products.schema import ProductRead
from app.features.products.product_route import router
from app.features.products.dependency import get_product_by_id_use_case
from app.features.products.use_cases.get_product_by_id import GetProductByIdUseCase

from fastapi import status, Depends, Path
from typing import Annotated

@router.get(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductRead,
    summary="Get an Product by her id"
)
async def get_product_by_id(
    product_id: Annotated[int, Path(title="The product's id to get it.")],
    use_case: Annotated[GetProductByIdUseCase, Depends(get_product_by_id_use_case)]
) -> ProductRead:
    
    product = await use_case.execute(product_id)

    return ProductRead.model_validate(product)