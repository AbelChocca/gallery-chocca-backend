from app.infra.db.uow.dependency import get_uow
from app.infra.db.uow.unit_of_work import UnitOfWork
from app.features.balancing.services.other_current_liability_service import OtherCurrentLiabilityService

from fastapi import Depends


def get_other_current_liability_service(
    uow: UnitOfWork = Depends(get_uow),
) -> OtherCurrentLiabilityService:

    return OtherCurrentLiabilityService(
        other_current_liability_repository=uow.other_current_liabilities,
    )
