from typing import Annotated

from fastapi import Depends

from app.features.orders.services.order_service import (
    OrderService,
)
from app.features.orders.services.order_billing_service import (
    OrderBillingService,
)
from app.features.orders.services.order_item_service import (
    OrderItemService,
)
from app.features.orders.services.order_receipt import (
    OrderReceiptService,
)

from app.features.receipts.services.receipt_service import (
    ReceiptService,
)

from app.features.mail.services.mail_service import (
    MailService,
)

from app.features.orders.dependencies.services import (
    get_order_service,
    get_order_billing_service,
    get_order_item_service,
    get_order_receipt_service
)

from app.features.receipts.dependencies.services import (
    get_receipt_service,
)

from app.features.mail.dependencies.services import (
    get_mail_service,
)

from app.features.receipts.use_cases.generate_receipt import (
    GenerateReceiptUseCase,
)


def get_generate_receipt_use_case(
    order_service: Annotated[
        OrderService,
        Depends(get_order_service),
    ],
    order_billing_service: Annotated[
        OrderBillingService,
        Depends(get_order_billing_service),
    ],
    order_item_service: Annotated[
        OrderItemService,
        Depends(get_order_item_service),
    ],
    order_receipt_service: Annotated[
        OrderReceiptService,
        Depends(get_order_receipt_service),
    ],
    receipt_service: Annotated[
        ReceiptService,
        Depends(get_receipt_service),
    ],
    mail_service: Annotated[
        MailService,
        Depends(get_mail_service),
    ],
) -> GenerateReceiptUseCase:

    return GenerateReceiptUseCase(
        order_service=order_service,
        order_billing_service=order_billing_service,
        order_item_service=order_item_service,
        order_receipt_service=order_receipt_service,
        receipt_service=receipt_service,
        mail_service=mail_service,
    )