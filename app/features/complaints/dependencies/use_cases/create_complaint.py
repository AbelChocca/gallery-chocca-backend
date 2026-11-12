
from typing import Annotated

from fastapi import Depends

from app.infra.db.uow.dependency import (
    UnitOfWork,
    get_uow,
)

from app.features.complaints.services.complaint_service import (
    ComplaintService,
)
from app.features.complaints.dependencies.services import (
    get_complaint_service,
)

from app.features.complaints.types.complaint import (
    ComplaintProviderIdentity,
)
from app.features.complaints.dependencies.provider import (
    get_complaint_provider,
)

from app.features.mail.services.mail_service import (
    MailService,
)
from app.features.mail.dependencies.services import (
    get_mail_service,
)

from app.features.complaints.use_cases.create_complaint import (
    CreateComplaintUseCase,
)

from app.shared.calendar.business_day_service import get_business_day_service, BusinessDayService


def get_create_complaint_use_case(
    complaint_service: Annotated[
        ComplaintService,
        Depends(get_complaint_service),
    ],
    business_day_service: Annotated[
        BusinessDayService,
        Depends(get_business_day_service),
    ],
    mail_service: Annotated[
        MailService,
        Depends(get_mail_service),
    ],
    provider: Annotated[
        ComplaintProviderIdentity,
        Depends(get_complaint_provider),
    ],
    uow: Annotated[
        UnitOfWork,
        Depends(get_uow),
    ],
) -> CreateComplaintUseCase:

    return CreateComplaintUseCase(
        complaint_service=complaint_service,
        business_day_service=business_day_service,
        mail_service=mail_service,
        provider=provider,
        uow=uow,
    )
