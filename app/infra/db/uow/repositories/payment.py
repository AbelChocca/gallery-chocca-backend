# app/infra/db/uow/repositories/payments.py

from app.features.payments.repositories.payment_repository import (
    PaymentRepository,
)
from app.features.payments.models.payment import (
    PaymentTable,
)
from app.features.payments.mappers.payment import (
    PaymentMapper,
)

from app.features.payments.repositories.payment_event_repository import (
    PaymentEventRepository,
)
from app.features.payments.models.payment_events import (
    PaymentEventTable,
)
from app.features.payments.mappers.payment_event import (
    PaymentEventMapper,
)


class PaymentsRepositoriesMixin:

    @property
    def payments(
        self,
    ) -> PaymentRepository:
        return self._get_or_create(
            "payments",
            lambda: PaymentRepository(
                self.session,
                PaymentMapper,
                PaymentTable,
            ),
        )

    @property
    def payment_events(
        self,
    ) -> PaymentEventRepository:
        return self._get_or_create(
            "payment_events",
            lambda: PaymentEventRepository(
                self.session,
                PaymentEventMapper,
                PaymentEventTable,
            ),
        )