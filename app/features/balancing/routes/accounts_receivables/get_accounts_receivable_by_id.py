from fastapi import Depends

from app.features.balancing.dependencies.accounts_receivable.service import (
    get_accounts_receivable_service,
)
from app.features.balancing.routes.accounts_receivables.account_receivable_router import (
    accounts_receivable_router,
)
from app.features.balancing.schemas.accounts_receivable_schema import (
    AccountsReceivableResponseSchema,
)
from app.features.balancing.services.accounts_receivable_service import (
    AccountsReceivableService,
)


@accounts_receivable_router.get(
    "/{account_receivable_id}",
    response_model=AccountsReceivableResponseSchema,
)
async def get_accounts_receivable_by_id(
    account_receivable_id: int,
    service: AccountsReceivableService = Depends(
        get_accounts_receivable_service
    ),
) -> AccountsReceivableResponseSchema:

    account_receivable = await service.get_by_id(
        account_receivable_id
    )

    return AccountsReceivableResponseSchema.model_validate(
        account_receivable
    )