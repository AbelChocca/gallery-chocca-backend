from app.infra.db.uow.dependency import get_uow
from app.infra.db.uow.unit_of_work import UnitOfWork
from app.shared.pagination.pagination_service import get_pagination_service, PaginationService
from app.features.balancing.services.accounts_payable_service import AccountsPayableService

from fastapi import Depends

def get_accounts_payable_service(
    uow: UnitOfWork = Depends(get_uow),
    pagination: PaginationService = Depends(
        get_pagination_service
    ),
) -> AccountsPayableService:

    return AccountsPayableService(
        accounts_payable_repository=uow.accounts_payable,
        pagination_service=pagination,
    )