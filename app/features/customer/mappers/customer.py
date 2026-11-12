from app.features.customer.entities.customer import CustomerEntity
from app.features.customer.models.customer import Customer

from app.infra.db.mappers.base_mapper import BaseMapper


class CustomerMapper(
    BaseMapper[
        CustomerEntity,
        Customer,
    ]
):

    @staticmethod
    def to_entity(
        model: Customer,
    ) -> CustomerEntity:
        return CustomerEntity(
            id=model.id,
            user_id=model.user_id,
            session_id=model.session_id,
            name=model.name,
            last_name=model.last_name,
            customer_type=model.customer_type,
            document_type=model.document_type,
            document_number=model.document_number,
            email=model.email,
            phone=model.phone,
            address=model.address,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_db_model(
        entity: CustomerEntity,
        existing_model: Customer | None = None,
    ) -> Customer:
        model = existing_model or Customer()

        model.id = entity.id

        model.user_id = entity.user_id
        model.session_id = entity.session_id

        model.name = entity.name
        model.last_name = entity.last_name

        model.customer_type = entity.customer_type

        model.document_type = (
            entity.document_type
        )

        model.document_number = (
            entity.document_number
        )

        model.email = entity.email
        model.phone = entity.phone
        model.address = entity.address

        model.created_at = entity.created_at
        model.updated_at = entity.updated_at

        return model