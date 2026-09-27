from app.features.customer.customer_repository import (
    CustomerRepository,
)
from app.features.customer.mappers.customer import (
    CustomerMapper,
)
from app.features.customer.models.customer import (
    Customer as CustomerTable,
)


class CustomerRepositoriesMixin:

    @property
    def customers(
        self,
    ) -> CustomerRepository:
        return self._get_or_create(
            "customers",
            lambda: CustomerRepository(
                self.session,
                CustomerMapper,
                CustomerTable,
            ),
        )