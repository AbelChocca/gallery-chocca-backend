# app/features/payments/routes/webhook_routes.py

from typing import Annotated, Any

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from app.features.payments.dependencies.use_cases.openpay_webhook import (
    get_process_openpay_webhook_use_case,
)

from app.features.payments.schemas.openpay_schema import (
    OpenpayWebhookSchema,
)

from app.features.payments.use_cases.openpay_webhook import (
    ProcessOpenpayWebhookUseCase,
)


router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks"],
)


@router.post(
    "/openpay",
    status_code=status.HTTP_200_OK,
)
async def openpay_webhook(
    payload: dict[str, Any],

    use_case: Annotated[
        ProcessOpenpayWebhookUseCase,
        Depends(
            get_process_openpay_webhook_use_case
        ),
    ],
):
    if not payload:
        return {
            "received": True,
        }

    if payload["type"] == "verification":
        return

    
    event = OpenpayWebhookSchema.model_validate(
        payload
    )

    await use_case.execute(
        event
    )

    return {
        "received": True,
    }