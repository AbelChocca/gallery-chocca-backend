from typing import Annotated

import httpx

from fastapi import Depends

from app.core.http_dependency import (
    get_http_client,
)

from app.features.receipts.providers.base import (
    ReceiptProvider,
)

from app.features.receipts.providers.factusmart import (
    FactuSmartReceiptProvider,
)


def get_receipt_provider(
) -> ReceiptProvider:

    return FactuSmartReceiptProvider(
    )