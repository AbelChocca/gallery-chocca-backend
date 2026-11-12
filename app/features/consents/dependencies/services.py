from fastapi import Depends

from app.features.consents.consent_service import (
    ConsentService,
)
from app.infra.db.uow.dependency import get_uow
from app.infra.db.uow.unit_of_work import UnitOfWork


def get_consent_service(
    uow: UnitOfWork = Depends(get_uow),
) -> ConsentService:
    return ConsentService(
        consent_repository=uow.consents,
    )