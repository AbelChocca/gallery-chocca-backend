from typing import Annotated

from fastapi import Depends

from app.features.complaints.services.complaint_service import (
    ComplaintService,
)
from app.features.complaints.services.complaint_response_service import (
    ComplaintResponseService,
)

from app.features.complaints.dependencies.services import (
    get_complaint_service,
    get_complaint_response_service,
)

from app.features.complaints.use_cases.send_admin_complaint_response import (
    SendAdminComplaintResponseUseCase,
)

from app.features.mail.services.mail_service import (
    MailService,
)
from app.features.mail.dependencies.services import (
    get_mail_service,
)
from app.infra.db.uow.dependency import (
    UnitOfWork,
    get_uow,
)


def get_send_admin_complaint_response_use_case(
    complaint_service: Annotated[
        ComplaintService,
        Depends(get_complaint_service),
    ],
    complaint_response_service: Annotated[
        ComplaintResponseService,
        Depends(get_complaint_response_service),
    ],
    mail_service: Annotated[
        MailService,
        Depends(get_mail_service),
    ],
    uow: Annotated[
        UnitOfWork,
        Depends(get_uow),
    ],
) -> SendAdminComplaintResponseUseCase:

    return SendAdminComplaintResponseUseCase(
        complaint_service=complaint_service,
        complaint_response_service=complaint_response_service,
        mail_service=mail_service,
        uow=uow,
    )
