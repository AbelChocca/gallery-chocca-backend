from fastapi import Depends, status

from app.features.balancing.dependencies.accounts_receivable.service import (
    get_accounts_receivable_service,
)
from app.features.balancing.services.accounts_receivable_service import (
    AccountsReceivableService,
)
from app.features.balancing.routes.accounts_receivables.account_receivable_router import (
    accounts_receivable_router,
)


@accounts_receivable_router.delete(
    "/{accounts_receivable_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_accounts_receivable(
    accounts_receivable_id: int,
    service: AccountsReceivableService = Depends(
        get_accounts_receivable_service
    ),
) -> None:

    await service.delete(accounts_receivable_id)