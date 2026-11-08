# app/features/checkout/routes.py

from datetime import UTC, datetime
from typing import Annotated

from fastapi import (
    Depends,
    status,
)

from app.api.security.resolvers.session_owner import (
    OwnerSession,
    get_session_owner,
)
from app.features.orders.checkout_router import (
    router,
)
from app.features.orders.dependencies.use_cases.checkout_preview import (
    get_checkout_preview_use_case,
)
from app.features.orders.schemas.checkout import (
    CheckoutPreviewRequest,
    CheckoutPreviewResponse
)
from app.features.orders.use_cases.checkout_preview import (
    CheckoutPreviewUseCase,
)
from app.features.customer.dtos.customer import (
    CustomerPricingContext,
)
from app.features.customer.helpers.get_customer_pricing_context import (
    get_customer_pricing_context,
)
from app.features.orders.types.shipping import ShippingLocationDTO


@router.post(
    "/preview",
    response_model=CheckoutPreviewResponse | None,
    status_code=status.HTTP_200_OK,
    summary="Preview checkout",
)
async def checkout_preview(
    payload: CheckoutPreviewRequest,
    use_case: Annotated[
        CheckoutPreviewUseCase,
        Depends(get_checkout_preview_use_case),
    ],
    owner: Annotated[
        OwnerSession,
        Depends(get_session_owner),
    ],
    customer: Annotated[
        CustomerPricingContext | None,
        Depends(get_customer_pricing_context),
    ],
) -> CheckoutPreviewResponse | None:
    now = datetime.now(UTC)

    result = await use_case.execute(
        user_id=owner.user_id,
        session_id=owner.session_id,
        customer_id=(
            customer.customer_id
            if customer
            else None
        ),
        customer_type=(
            customer.customer_type
            if customer
            else None
        ),
        coupon_code=payload.coupon_code,
        payment_method=payload.payment_method,
        shipping_location=(
            ShippingLocationDTO(
                **payload.shipping_location.model_dump()
            )
            if payload.shipping_location
            else None
        ),
        delivery_method=payload.delivery_method,
        pickup_location_id=payload.pickup_location_id,
        now=now,
    )

    if result is None:
        return None

    return CheckoutPreviewResponse.model_validate(
        result
    )