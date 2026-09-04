from app.infra.db.uow.dependency import get_uow
from app.infra.db.uow.unit_of_work import UnitOfWork
from app.features.balancing.services.accounts_receivable_service import AccountsReceivableService

from fastapi import Depends

def get_accounts_receivable_service(
    uow: UnitOfWork = Depends(get_uow),
) -> AccountsReceivableService:

    return AccountsReceivableService(
        accounts_receivable_repository=uow.accounts_receivable,
    )