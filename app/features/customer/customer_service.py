from app.features.customer.dtos.customer import (
    CustomerSearchOptionDTO,
    CustomerFilters
)
from app.features.customer.customer_repository import (
    CustomerRepository,
)

from app.shared.pagination.dto import (
    PaginatedDTO,
)
from app.shared.pagination.pagination_service import (
    PaginationService,
)
from app.features.customer.entities.customer import CustomerEntity
from app.features.customer.customer_types import CustomerType, IdentityDocumentType
from datetime import datetime

class CustomerService:

    def __init__(
        self,
        customer_repository: CustomerRepository,
        pagination_service: PaginationService,
    ):
        self.customer_repository = customer_repository
        self.pagination_service = pagination_service

    async def create(
        self,
        user_id: int,
        session_id: str,
        name: str,
        last_name: str,
        document_type: IdentityDocumentType | None = None,
        document_number: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        address: str | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None
    ) -> CustomerEntity:
        customer = CustomerEntity(
            user_id=user_id,
            customer_type=CustomerType.REGULAR,
            session_id=session_id,
            document_type=document_type,
            document_number=document_number,
            name=name,
            last_name=last_name,
            email=email,
            address=address,
            phone=phone,
            created_at=created_at,
            updated_at=updated_at
        )
        return await self.customer_repository.save(customer)

    async def get_by_user_id(
        self,
        user_id: int,
    ) -> CustomerEntity | None:
        return await self.customer_repository.get_by_user_id(
            user_id
        )

    async def get_by_session_id(
        self,
        session_id: str,
    ) -> CustomerEntity | None:
        return await self.customer_repository.get_by_session_id(
            session_id
        )

    async def search_options(
        self,
        *,
        search: str | None,
        page: int,
        limit: int,
    ) -> PaginatedDTO[
        CustomerSearchOptionDTO
    ]:
        offset = (
            self.pagination_service.get_offset(
                page=page,
                limit=limit,
            )
        )

        items, total_items = (
            await self.customer_repository.search_options(
                search=search,
                offset=offset,
                limit=limit,
            )
        )

        total_pages = (
            self.pagination_service.get_total_pages(
                total=total_items,
                limit=limit,
            )
        )

        current_page = (
            self.pagination_service.get_current_page(
                offset=offset,
                limit=limit,
            )
        )

        return PaginatedDTO.create(
            items=items,
            total_items=total_items,
            current_page=current_page,
            total_pages=total_pages,
        )

    async def get_customers(
        self,
        *,
        filters: CustomerFilters,
        page: int,
        limit: int,
    ) -> PaginatedDTO[CustomerSearchOptionDTO]:

        offset = self.pagination_service.get_offset(
            page=page,
            limit=limit,
        )

        items, total_items = (
            await self.customer_repository.get_customers(
                filters=filters,
                offset=offset,
                limit=limit,
            )
        )

        total_pages = (
            self.pagination_service.get_total_pages(
                total=total_items,
                limit=limit,
            )
        )

        current_page = (
            self.pagination_service.get_current_page(
                offset=offset,
                limit=limit,
            )
        )

        return PaginatedDTO.create(
            items=items,
            total_items=total_items,
            current_page=current_page,
            total_pages=total_pages,
        )

    async def get_by_id(
        self,
        customer_id: int,
    ) -> CustomerEntity | None:
        return await self.customer_repository.get_by_id(
            customer_id
        )