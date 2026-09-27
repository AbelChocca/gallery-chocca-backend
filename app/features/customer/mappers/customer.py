from app.features.customer.entities.customer import (
    CustomerEntity,
)
from app.features.customer.models.customer import Customer

from app.infra.db.mappers.base_mapper import BaseMapper


class CustomerMapper(
    BaseMapper[
        Customer,
        CustomerEntity,
    ]
):
    @staticmethod
    def to_entity(
        model: Customer,
    ) -> CustomerEntity:
        return CustomerEntity(
            id=model.id,
            name=model.name,
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
    def to_model(
        entity: CustomerEntity,
    ) -> Customer:
        return Customer(
            id=entity.id,
            name=entity.name,
            customer_type=entity.customer_type,
            document_type=entity.document_type,
            document_number=entity.document_number,
            email=entity.email,
            phone=entity.phone,
            address=entity.address,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )