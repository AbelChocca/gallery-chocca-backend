from fastapi import Depends, status

from app.features.balancing.dependencies.accounts_receivable.service import (
    get_accounts_receivable_service,
)
from app.features.balancing.types.accounts_receivable_types import (
    AccountsReceivableUpdate,
)
from app.features.balancing.routes.accounts_receivables.account_receivable_router import (
    accounts_receivable_router,
)
from app.features.balancing.schemas.accounts_receivable_schema import (
    AccountsReceivableUpdateSchema,
)
from app.features.balancing.services.accounts_receivable_service import (
    AccountsReceivableService,
)


@accounts_receivable_router.put(
    "/{accounts_receivable_id}",
    status_code=status.HTTP_200_OK,
)
async def update_accounts_receivable(
    accounts_receivable_id: int,
    payload: AccountsReceivableUpdateSchema,
    service: AccountsReceivableService = Depends(get_accounts_receivable_service),
):
    update_dto = AccountsReceivableUpdate(
        brand=payload.brand,
        entity_name=payload.entity_name,
        location=payload.location,
        amount=payload.amount,
        status=payload.status,
        fields_set=payload.model_fields_set
    )

    return await service.update(
        accounts_receivable_id,
        update_dto,
    )