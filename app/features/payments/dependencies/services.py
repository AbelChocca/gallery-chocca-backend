from typing import Annotated

from fastapi import Depends

from app.features.payments.dependencies.providers.openpay import get_payment_provider
from app.infra.db.uow.dependency import get_uow, UnitOfWork
from app.features.payments.services.payment_service import PaymentService
from app.features.payments.providers.base_provider import BasePaymentProvider
from app.features.payments.services.payment_event_service import PaymentEventService


def get_payment_service(
    uow: Annotated[
        UnitOfWork,
        Depends(get_uow),
    ],
    payment_provider: Annotated[
        BasePaymentProvider,
        Depends(get_payment_provider),
    ],
) -> PaymentService:
    return PaymentService(
        payment_repository=uow.payments,
        payment_provider=payment_provider,
    )

def get_payment_event_service(
    uow: Annotated[
        UnitOfWork,
        Depends(get_uow),
    ],
) -> PaymentEventService:
    return PaymentEventService(
        repository=uow.payment_events,
    )