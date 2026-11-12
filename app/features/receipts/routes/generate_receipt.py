from typing import Annotated

from fastapi import Depends, Query, status

from app.features.receipts.receipt_route import router
from app.features.receipts.dependencies.use_cases.generate_receipt import (
    get_generate_receipt_use_case,
)
from app.features.receipts.use_cases.generate_receipt import (
    GenerateReceiptUseCase,
)
from app.features.receipts.schemas.receipt import (
    IssuedReceiptResponse,
)

from app.core.authorization.dependencies import (
    require_permission,
)
from app.core.authorization.permissions import (
    Permission,
)


@router.post(
    "/orders/{order_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Generate order receipt",
    dependencies=[
        require_permission(
            Permission.RECEIPT_GENERATE
        )
    ],
    response_model=IssuedReceiptResponse,
)
async def generate_receipt(
    order_id: int,
    case: Annotated[
        GenerateReceiptUseCase,
        Depends(get_generate_receipt_use_case),
    ],
    send_to_mail: Annotated[
        bool,
        Query(),
    ] = True,
) -> IssuedReceiptResponse:

    result = await case.execute(
        order_id=order_id,
        send_to_mail=send_to_mail,
    )

    return IssuedReceiptResponse.model_validate(
        result
    )