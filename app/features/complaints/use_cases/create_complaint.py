from dataclasses import dataclass
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from app.features.complaints.services.complaint_service import (
    ComplaintService,
)
from app.features.complaints.types.complaint import (
    CreateComplaintInput,
    CreateComplaintResult,
    ComplaintResponseChannel,
    ComplaintProviderIdentity
)

from app.features.mail.services.mail_service import MailService
from app.features.mail.types.mail import SendMailDTO

from app.features.mail.templates.complaint_receipt import (
    ComplaintReceiptMailTemplate,
    ComplaintReceiptMailTemplateData,
)

from app.shared.calendar.business_day_service import (
    BusinessDayService,
)
from app.infra.db.uow.unit_of_work import UnitOfWork
from app.core.exceptions import AppException
from app.core.log.config import logger_service


class CreateComplaintUseCase:
    def __init__(
        self,
        *,
        complaint_service: ComplaintService,
        business_day_service: BusinessDayService,
        mail_service: MailService,
        uow:UnitOfWork,
        provider: ComplaintProviderIdentity,
    ):
        self._complaint_service = complaint_service
        self._business_day_service = business_day_service
        self._mail_service = mail_service
        self._uow = uow
        self._provider = provider

    async def execute(
        self,
        *,
        input: CreateComplaintInput,
    ) -> CreateComplaintResult:
        now = datetime.now(timezone.utc)

        peru_now = now.astimezone(
            ZoneInfo("America/Lima")
        )

        response_due_at = (
            self._business_day_service.add_business_days(
                current=peru_now,
                days=15,
            )
        ).astimezone(timezone.utc)

        # 1. Registrar la reclamación
        complaint = await self._complaint_service.create(
            provider_legal_name=self._provider.legal_name,
            provider_ruc=self._provider.ruc,
            provider_address=self._provider.address,

            first_name=input.first_name,
            last_name=input.last_name,
            document_type=input.document_type,
            document_number=input.document_number,
            email=input.email,
            phone=input.phone,
            address=input.address,

            is_minor=input.is_minor,
            representative_name=input.representative_name,
            representative_document=(
                input.representative_document
            ),

            good_type=input.good_type,
            order_number=input.order_number,
            amount=input.amount,
            product_description=input.product_description,

            complaint_type=input.complaint_type,
            detail=input.detail,
            requested_solution=input.requested_solution,
            response_channel=input.response_channel,

            response_due_at=response_due_at,
            now=now,
        )

        await self._uow.commit()

        email_sent = False

        if (
            input.response_channel
            == ComplaintResponseChannel.EMAIL
            and input.email is not None
        ):
            template_data = ComplaintReceiptMailTemplateData(
                recipient_name=(
                    f"{complaint.first_name} "
                    f"{complaint.last_name}"
                ).strip(),
                complaint_number=complaint.complaint_number,
                complaint_type=complaint.complaint_type.value,
                created_at=complaint.created_at,
            )

            try:
                await self._mail_service.send(
                    payload=SendMailDTO(
                        to=input.email,
                        subject=ComplaintReceiptMailTemplate.subject(
                            template_data
                        ),
                        html=ComplaintReceiptMailTemplate.render_html(
                            template_data
                        ),
                    )
                )

                email_sent = True

            except Exception as exc:
                logger_service.error(
                    "Complaint receipt email failed. "
                    "complaint_number={} error_type={}",
                    complaint.complaint_number,
                    type(exc).__name__,
                )

        return CreateComplaintResult(
            public_id=complaint.public_id,
            complaint_number=complaint.complaint_number,
            status=complaint.status,
            created_at=complaint.created_at,
            receipt_email_sent=email_sent,
        )
