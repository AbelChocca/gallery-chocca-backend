from app.core.exceptions import InvalidOperation

from app.infra.db.uow.dependency import UnitOfWork

from app.features.complaints.services.complaint_service import (
    ComplaintService,
)
from app.features.complaints.services.complaint_response_service import (
    ComplaintResponseService,
)

from app.features.complaints.types.complaint import (
    ComplaintResponseChannel,
    ComplaintStatus,
)
from app.features.complaints.entities.complaint_response import (
    ComplaintResponse,
)

from app.features.mail.services.mail_service import MailService
from app.features.mail.types.mail import SendMailDTO

from app.features.mail.templates.complaint_response import (
    ComplaintResponseMailTemplate,
    ComplaintResponseMailTemplateData,
)

from app.core.log.loguru_service import logger_service
from app.core.settings.pydantic_settings import settings
from app.core.app_exception import AppException


class SendAdminComplaintResponseUseCase:

    def __init__(
        self,
        *,
        complaint_service: ComplaintService,
        complaint_response_service: ComplaintResponseService,
        mail_service: MailService,
        uow: UnitOfWork,
    ):
        self._complaint_service = complaint_service
        self._complaint_response_service = complaint_response_service
        self._mail_service = mail_service
        self._uow = uow

    async def execute(
        self,
        *,
        complaint_id: int,
        response_id: int,
    ) -> ComplaintResponse:

        # 1. Bloquear y validar la reclamación
        complaint = await self._complaint_service.get_by_id(
            complaint_id=complaint_id,
            raises=True,
            with_lock=True,
        )

        if complaint.response_channel != ComplaintResponseChannel.EMAIL:
            raise InvalidOperation(
                message=(
                    "Esta reclamación requiere respuesta por CARTA. "
                    "No se puede enviar mediante correo electrónico."
                ),
            )

        if complaint.status == ComplaintStatus.RESPONDED:
            raise InvalidOperation(
                message="La reclamación ya fue respondida."
            )

        if not complaint.email:
            raise InvalidOperation(
                message="La reclamación no tiene correo de destino."
            )

        # 2. Reservar envío: DRAFT -> PENDING_SEND
        response = await self._complaint_response_service.reserve_send(
            response_id=response_id,
            complaint_id=complaint_id,
        )

        # Confirmar ANTES de llamar a Resend.
        await self._uow.session.commit()

        template_data = ComplaintResponseMailTemplateData(
            recipient_name=(
                f"{complaint.first_name} {complaint.last_name}"
            ).strip(),
            complaint_number=complaint.complaint_number,
            message=response.message,
            provider_name=complaint.provider_legal_name,
        )

        # 3. Enviar correo mediante tu MailService
        try:
            
            sent_mail = await self._mail_service.send(
                payload=SendMailDTO(
                    to=complaint.email,
                    subject=ComplaintResponseMailTemplate.subject(
                        template_data
                    ),
                    html=ComplaintResponseMailTemplate.render_html(
                        template_data
                    ),
                    from_email=settings.RESEND_COMPLAINTS_FROM_EMAIL,
                    reply_to=settings.COMPLAINT_REPLY_TO_EMAIL,
                )
            )


        except AppException:
            logger_service.exception(
                "Complaint response email failed."
                "complaint_id=%s response_id=%s",
                complaint_id,
                response_id,
            )

            raise 

        # 4. Registrar envío y actualizar reclamación
        response = await self._complaint_response_service.mark_sent(
            response_id=response_id,
            external_message_id=sent_mail.id,
        )

        await self._complaint_service.update_status(
            complaint_id=complaint_id,
            status=ComplaintStatus.RESPONDED,
        )

        return response
