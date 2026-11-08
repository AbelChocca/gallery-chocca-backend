from typing import Annotated

from fastapi import Depends, Path, status

from app.features.products.schema import ProductRead
from app.features.products.product_route import router
from app.features.products.dependency import (
    get_product_by_id_use_case,
)
from app.features.products.use_cases.get_product_by_id import (
    GetProductByIdUseCase,
)

from app.features.customer.dtos.customer import (
    CustomerPricingContext,
)
from app.features.customer.helpers.get_customer_pricing_context import (
    get_customer_pricing_context,
)


@router.get(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductRead,
    summary="Get product by ID",
)
async def get_product_by_id(
    product_id: Annotated[
        int,
        Path(gt=0, title="Product ID"),
    ],
    use_case: Annotated[
        GetProductByIdUseCase,
        Depends(get_product_by_id_use_case),
    ],
    customer: Annotated[
        CustomerPricingContext | None,
        Depends(get_customer_pricing_context),
    ],
) -> ProductRead:

    product = await use_case.execute(
        product_id=product_id,
        customer_id=(
            customer.customer_id
            if customer
            else None
        ),
        customer_type=(
            customer.customer_type
            if customer
            else None
        ),
    )

    return ProductRead.model_validate(product)