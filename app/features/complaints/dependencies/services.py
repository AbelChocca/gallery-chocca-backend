from typing import Annotated

from fastapi import Depends

# Ajusta este import a tu provider existente.
from app.infra.db.uow.dependency import get_uow, UnitOfWork

from app.features.complaints.services.complaint_service import (
    ComplaintService,
)
from app.features.complaints.services.complaint_response_service import (
    ComplaintResponseService,
)
from app.shared.pagination.pagination_service import PaginationService, get_pagination_service

def get_complaint_service(
    uow: Annotated[UnitOfWork, Depends(get_uow)],
    pagination_service: Annotated[
        PaginationService,
        Depends(get_pagination_service),
    ],
) -> ComplaintService:
    return ComplaintService(
        repository=uow.complaints,
        pagination_service=pagination_service,
    )


def get_complaint_response_service(
    uow: Annotated[
        UnitOfWork,
        Depends(get_uow),
    ],
) -> ComplaintResponseService:

    return ComplaintResponseService(
        repository=uow.complaint_responses,
    )
