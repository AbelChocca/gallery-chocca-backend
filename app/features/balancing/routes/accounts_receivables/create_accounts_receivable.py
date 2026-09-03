from fastapi import Depends, status

from app.features.balancing.dependencies.accounts_receivable.service import (
    get_accounts_receivable_service,
)
from app.features.balancing.entities.accounts_receivable import (
    AccountsReceivable,
)
from app.features.balancing.routes.accounts_receivables.account_receivable_router import (
    accounts_receivable_router,
)
from app.features.balancing.schemas.accounts_receivable_schema import (
    AccountsReceivableCreateSchema,
    AccountsReceivableResponseSchema,
)
from app.features.balancing.services.accounts_receivable_service import (
    AccountsReceivableService,
)


@accounts_receivable_router.post(
    "",
    response_model=AccountsReceivableResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_accounts_receivable(
    schema: AccountsReceivableCreateSchema,
    service: AccountsReceivableService = Depends(
        get_accounts_receivable_service
    ),
) -> AccountsReceivableResponseSchema:

    entity = AccountsReceivable(
        balance_snapshot_id=schema.balance_snapshot_id,
        brand=schema.brand,
        entity_name=schema.entity_name,
        location=schema.location,
        amount=schema.amount,
        status=schema.status,
    )

    account_receivable = await service.create(entity)

    return AccountsReceivableResponseSchema.model_validate(
        account_receivable
    )