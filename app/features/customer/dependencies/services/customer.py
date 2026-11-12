from fastapi import Depends

from app.features.customer.customer_service import (
    CustomerService,
)

from app.infra.db.uow.dependency import (
    get_uow,
)
from app.infra.db.uow.unit_of_work import (
    UnitOfWork,
)

from app.shared.pagination.pagination_service import (
    PaginationService,
    get_pagination_service,
)


def get_customer_service(
    uow: UnitOfWork = Depends(
        get_uow
    ),
    pagination_service: PaginationService = Depends(
        get_pagination_service
    ),
) -> CustomerService:
    return CustomerService(
        customer_repository=uow.customers,
        pagination_service=pagination_service,
    )