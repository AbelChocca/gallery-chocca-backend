from typing import Protocol

from app.features.payments.types.payment_provider import (
    CreateCheckoutRequest, CheckoutResult,
)
from app.features.payments.types.payment_provider import CreateCardChargeRequest, CardChargeResult


class BasePaymentProvider(Protocol):

    async def create_checkout(
        self,
        request: CreateCheckoutRequest,
    ) -> CheckoutResult:
        ...

    async def create_card_charge(
        self,
        request: CreateCardChargeRequest,
    ) -> CardChargeResult:
        ...