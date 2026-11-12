
from app.infra.db.mappers.base_mapper import BaseMapper

from app.features.complaints.entities.complaint_response import (
    ComplaintResponse,
)
from app.features.complaints.models.complaint_response import (
    ComplaintResponseTable,
)


class ComplaintResponseMapper(
    BaseMapper[ComplaintResponse, ComplaintResponseTable]
):

    @staticmethod
    def to_db_model(
        entity: ComplaintResponse,
        existing_model: ComplaintResponseTable | None = None,
    ) -> ComplaintResponseTable:
        model = existing_model or ComplaintResponseTable()

        model.id = entity.id
        model.complaint_id = entity.complaint_id
        model.author_user_id = entity.author_user_id

        model.message = entity.message
        model.status = entity.status

        model.recipient_email = entity.recipient_email
        model.external_message_id = entity.external_message_id
        model.error_message = entity.error_message

        model.physical_delivery_reference = (
            entity.physical_delivery_reference
        )

        if entity.created_at is not None:
            model.created_at = entity.created_at

        model.sent_at = entity.sent_at
        model.delivered_at = entity.delivered_at

        return model

    @staticmethod
    def to_entity(
        model: ComplaintResponseTable,
    ) -> ComplaintResponse:
        return ComplaintResponse(
            id=model.id,
            complaint_id=model.complaint_id,
            author_user_id=model.author_user_id,

            message=model.message,
            status=model.status,

            recipient_email=model.recipient_email,
            external_message_id=model.external_message_id,
            error_message=model.error_message,

            physical_delivery_reference=(
                model.physical_delivery_reference
            ),

            created_at=model.created_at,
            sent_at=model.sent_at,
            delivered_at=model.delivered_at,
        )
