from app.api.dependencies.products.case_depends import get_product_by_id_case
from app.api.schemas.products.schema import ProductRead
from app.api.v1.products.product_route import router
from app.application.products.cases.get_product_by_id import GetProductByIDCase

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
    case: Annotated[GetProductByIDCase, Depends(get_product_by_id_case)]
) -> ProductRead:
    product = await case.execute(product_id)
    return ProductRead(**product)