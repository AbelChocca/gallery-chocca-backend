from sqlalchemy import func, or_, select

from app.features.customer.entities.customer import (
    CustomerEntity,
)
from app.features.customer.dtos.customer import (
    CustomerSearchOptionDTO,
    CustomerPricingContext,
    CustomerFilters
)
from app.features.customer.models.customer import Customer

from app.infra.db.repositories.base_repository import (
    BaseRepository,
)


class CustomerRepository(
    BaseRepository[
        Customer,
        CustomerEntity,
    ]
):

    async def search_options(
        self,
        *,
        search: str | None,
        offset: int,
        limit: int,
    ) -> tuple[
        list[CustomerSearchOptionDTO],
        int,
    ]:
        filters = []

        if search:
            pattern = f"%{search.strip()}%"

            filters.append(
                or_(
                    Customer.name.ilike(pattern),
                    Customer.document_number.ilike(pattern),
                    Customer.email.ilike(pattern),
                    Customer.phone.ilike(pattern),
                )
            )

        count_statement = (
            select(func.count(Customer.id))
            .select_from(Customer)
            .where(*filters)
        )

        total_items = (
            await self._db_session.scalar(
                count_statement
            )
        ) or 0

        statement = (
            select(
                Customer.id,
                Customer.name,
                Customer.customer_type,
                Customer.document_type,
                Customer.document_number,
                Customer.email,
                Customer.phone,
            )
            .where(*filters)
            .order_by(
                Customer.name.asc(),
                Customer.id.asc(),
            )
            .offset(offset)
            .limit(limit)
        )

        result = await self._db_session.execute(
            statement
        )

        items = [
            CustomerSearchOptionDTO(
                id=row.id,
                name=row.name,
                customer_type=row.customer_type,
                document_type=row.document_type,
                document_number=row.document_number,
                email=row.email,
                phone=row.phone,
            )
            for row in result.all()
        ]

        return items, total_items

    async def get_pricing_context_by_user_id(
        self,
        *,
        user_id: int,
    ) -> CustomerPricingContext | None:

        statement = (
            select(
                Customer.id,
                Customer.customer_type,
            )
            .where(
                Customer.user_id == user_id
            )
        )

        result = await self._db_session.execute(
            statement
        )

        row = result.one_or_none()

        if row is None:
            return None

        return CustomerPricingContext(
            customer_id=row.id,
            customer_type=row.customer_type,
        )

    async def get_customers(
        self,
        *,
        filters: CustomerFilters,
        offset: int,
        limit: int,
    ) -> tuple[list[CustomerSearchOptionDTO], int]:

        conditions = []

        if filters.search:
            pattern = f"%{filters.search.strip()}%"

            conditions.append(
                or_(
                    Customer.name.ilike(pattern),
                    Customer.document_number.ilike(pattern),
                    Customer.email.ilike(pattern),
                    Customer.phone.ilike(pattern),
                )
            )

        if filters.customer_type is not None:
            conditions.append(
                Customer.customer_type
                == filters.customer_type
            )

        if filters.document_type is not None:
            conditions.append(
                Customer.document_type
                == filters.document_type
            )

        count_statement = (
            select(func.count(Customer.id))
            .select_from(Customer)
            .where(*conditions)
        )

        total_items = (
            await self._db_session.scalar(
                count_statement
            )
        ) or 0

        statement = (
            select(
                Customer.id,
                Customer.name,
                Customer.customer_type,
                Customer.document_type,
                Customer.document_number,
                Customer.email,
                Customer.phone,
            )
            .where(*conditions)
            .order_by(
                Customer.name.asc(),
                Customer.id.asc(),
            )
            .offset(offset)
            .limit(limit)
        )

        result = await self._db_session.execute(
            statement
        )

        items = [
            CustomerSearchOptionDTO(
                id=row.id,
                name=row.name,
                customer_type=row.customer_type,
                document_type=row.document_type,
                document_number=row.document_number,
                email=row.email,
                phone=row.phone,
            )
            for row in result.all()
        ]

        return items, total_items