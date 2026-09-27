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


class CustomerService:

    def __init__(
        self,
        customer_repository: CustomerRepository,
        pagination_service: PaginationService,
    ):
        self.customer_repository = customer_repository
        self.pagination_service = pagination_service

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