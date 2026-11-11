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