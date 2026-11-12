from typing import Annotated

from fastapi import Depends

from app.features.receipts.providers.base import (
    ReceiptProvider,
)

from app.features.receipts.dependencies.providers.factusmart import (
    get_receipt_provider,
)

from app.features.receipts.services.receipt_service import (
    ReceiptService,
)


def get_receipt_service(
    provider: Annotated[
        ReceiptProvider,
        Depends(get_receipt_provider),
    ],
) -> ReceiptService:

    return ReceiptService(
        provider=provider,
    )