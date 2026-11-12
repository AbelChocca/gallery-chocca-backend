
from app.infra.db.mappers.base_mapper import BaseMapper

from app.features.complaints.entities.complaint import Complaint
from app.features.complaints.models.complaint import ComplaintTable


class ComplaintMapper(BaseMapper[Complaint, ComplaintTable]):

    @staticmethod
    def to_db_model(
        entity: Complaint,
        existing_model: ComplaintTable | None = None,
    ) -> ComplaintTable:
        model = existing_model or ComplaintTable()

        model.id = entity.id
        model.public_id = entity.public_id
        model.complaint_number = entity.complaint_number

        model.provider_legal_name = entity.provider_legal_name
        model.provider_ruc = entity.provider_ruc
        model.provider_address = entity.provider_address

        model.first_name = entity.first_name
        model.last_name = entity.last_name
        model.document_type = entity.document_type
        model.document_number = entity.document_number
        model.email = entity.email
        model.phone = entity.phone
        model.address = entity.address

        model.is_minor = entity.is_minor
        model.representative_name = entity.representative_name
        model.representative_document = entity.representative_document

        model.good_type = entity.good_type
        model.order_number = entity.order_number
        model.amount = entity.amount
        model.product_description = entity.product_description

        model.complaint_type = entity.complaint_type
        model.detail = entity.detail
        model.requested_solution = entity.requested_solution

        model.response_channel = entity.response_channel
        model.status = entity.status
        model.assigned_to_user_id = entity.assigned_to_user_id

        if entity.created_at is not None:
            model.created_at = entity.created_at

        if entity.updated_at is not None:
            model.updated_at = entity.updated_at

        model.response_due_at = entity.response_due_at
        model.responded_at = entity.responded_at

        return model

    @staticmethod
    def to_entity(model: ComplaintTable) -> Complaint:
        return Complaint(
            id=model.id,
            public_id=model.public_id,
            complaint_number=model.complaint_number,

            provider_legal_name=model.provider_legal_name,
            provider_ruc=model.provider_ruc,
            provider_address=model.provider_address,

            first_name=model.first_name,
            last_name=model.last_name,
            document_type=model.document_type,
            document_number=model.document_number,
            email=model.email,
            phone=model.phone,
            address=model.address,

            is_minor=model.is_minor,
            representative_name=model.representative_name,
            representative_document=model.representative_document,

            good_type=model.good_type,
            order_number=model.order_number,
            amount=model.amount,
            product_description=model.product_description,

            complaint_type=model.complaint_type,
            detail=model.detail,
            requested_solution=model.requested_solution,

            response_channel=model.response_channel,
            status=model.status,
            assigned_to_user_id=model.assigned_to_user_id,

            created_at=model.created_at,
            updated_at=model.updated_at,
            response_due_at=model.response_due_at,
            responded_at=model.responded_at,
        )
