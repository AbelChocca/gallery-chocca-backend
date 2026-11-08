from typing import Annotated

import httpx
from fastapi import Depends

from app.features.payments.providers.openpay.openpay_provider import (
    OpenpayPaymentProvider,
)
from app.features.payments.providers.base_provider import BasePaymentProvider
from app.core.http_dependency import get_http_client

def get_payment_provider(
    client: Annotated[
        httpx.AsyncClient,
        Depends(get_http_client),
    ],
) -> BasePaymentProvider:
    return OpenpayPaymentProvider(
        client=client,
    )