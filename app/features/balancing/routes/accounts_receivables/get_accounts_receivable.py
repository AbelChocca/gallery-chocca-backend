from fastapi import Depends

from app.features.balancing.dependencies.accounts_receivable.service import (
    get_accounts_receivable_service,
)
from app.features.balancing.routes.accounts_receivables.account_receivable_router import (
    accounts_receivable_router,
)
from app.features.balancing.schemas.accounts_receivable_schema import (
    AccountsReceivableResponseSchema,
    AccountsReceivableFilters
)
from app.features.balancing.services.accounts_receivable_service import (
    AccountsReceivableService,
)


@accounts_receivable_router.get(
    "",
    response_model=list[AccountsReceivableResponseSchema],
)
async def get_accounts_receivable(
    filters: AccountsReceivableFilters = Depends(),
    service: AccountsReceivableService = Depends(
        get_accounts_receivable_service
    ),
) -> list[AccountsReceivableResponseSchema]:

    accounts_receivable = await service.find(
        balance_snapshot_id=filters.balance_snapshot_id,
        brand=filters.brand,
        entity_name=filters.entity_name,
        location=filters.location,
        status=filters.status,
    )

    return [
        AccountsReceivableResponseSchema.model_validate(
            account_receivable
        )
        for account_receivable in accounts_receivable
    ]