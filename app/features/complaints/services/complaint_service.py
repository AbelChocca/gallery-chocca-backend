from datetime import (
    datetime,
    timezone,
)
from decimal import Decimal
from uuid import uuid4
from dataclasses import replace

from app.features.complaints.entities.complaint import Complaint
from app.features.complaints.repositories.complaint_repository import (
    ComplaintRepository,
)
from app.features.complaints.types.complaint import (
    ComplaintType,
    ComplaintGoodType,
    ComplaintDocumentType,
    ComplaintResponseChannel,
    ComplaintStatus,
    AdminComplaintListItemDTO,
    ComplaintFilters,
)
from app.shared.pagination.pagination_service import PaginationService
from app.shared.pagination.dto import PaginatedDTO
from app.shared.datetime import to_datetime_range

class ComplaintService:

    def __init__(
        self,
        repository: ComplaintRepository,
        pagination_service: PaginationService,
    ):
        self._repository = repository
        self._pagination_service = pagination_service

    async def create(
        self,
        *,
        provider_legal_name: str,
        provider_ruc: str,
        provider_address: str,

        first_name: str,
        last_name: str,
        document_type: ComplaintDocumentType,
        document_number: str,
        email: str | None,
        phone: str | None,
        address: str,

        is_minor: bool,
        representative_name: str | None,
        representative_document: str | None,

        good_type: ComplaintGoodType,
        order_number: str | None,
        amount: Decimal | None,
        product_description: str,

        complaint_type: ComplaintType,
        detail: str,
        requested_solution: str,
        response_channel: ComplaintResponseChannel,

        response_due_at: datetime,
        now: datetime | None = None,
    ) -> Complaint:
        now = now or datetime.now(timezone.utc)

        sequence = (
            await self._repository.next_complaint_sequence()
        )

        complaint = Complaint(
            complaint_number=Complaint.generate_complaint_number(
                sequence,
                now,
            ),
            public_id=uuid4(),

            provider_legal_name=provider_legal_name,
            provider_ruc=provider_ruc,
            provider_address=provider_address,

            first_name=first_name,
            last_name=last_name,
            document_type=document_type,
            document_number=document_number,
            email=email,
            phone=phone,
            address=address,

            is_minor=is_minor,
            representative_name=representative_name,
            representative_document=representative_document,

            good_type=good_type,
            order_number=order_number,
            amount=amount,
            product_description=product_description,

            complaint_type=complaint_type,
            detail=detail,
            requested_solution=requested_solution,
            response_channel=response_channel,

            status=ComplaintStatus.SUBMITTED,

            created_at=now,
            updated_at=now,
            response_due_at=response_due_at,
        )

        return await self._repository.save(
            complaint,
            flush=True,
        )

    async def get_by_id(
        self,
        complaint_id: int,
        *,
        raises: bool = True,
        with_lock: bool = False,
    ) -> Complaint | None:
        return await self._repository.get_by_id(
            model_id=complaint_id,
            raises=raises,
            with_lock=with_lock,
        )

    async def get_by_public_id(
        self,
        public_id,
    ) -> Complaint | None:
        return await self._repository.get_by_public_id(
            public_id
        )

    async def get_by_id(
        self,
        complaint_id: int,
        *,
        raises: bool = True,
        with_lock: bool = False,
    ) -> Complaint | None:
        return await self._repository.get_by_id(
            model_id=complaint_id,
            raises=raises,
            with_lock=with_lock,
        )

    
    async def get_admin_complaints(
        self,
        *,
        filters: ComplaintFilters | None = None,
        page: int = 1,
        limit: int = 20,
    ) -> PaginatedDTO[AdminComplaintListItemDTO]:

        
        date_range = to_datetime_range(
            start=filters.created_at_from,
            end=filters.created_at_to,
        )

        normalized_filters = replace(
            filters,
            created_at_from=date_range.start,
            created_at_to=date_range.end,
        )


        offset = self._pagination_service.get_offset(
            page=page,
            limit=limit,
        )

        items, total_items = (
            await self._repository.get_admin_complaints(
                filters=normalized_filters,
                offset=offset,
                limit=limit,
            )
        )

        total_pages = self._pagination_service.get_total_pages(
            total=total_items,
            limit=limit,
        )

        current_page = self._pagination_service.get_current_page(
            offset=offset,
            limit=limit,
        )

        return PaginatedDTO.create(
            items=items,
            total_items=total_items,
            current_page=current_page,
            total_pages=total_pages,
        )

    async def update_status(
        self,
        *,
        complaint_id: int,
        status: ComplaintStatus,
        now: datetime | None = None,
    ) -> Complaint:
        complaint = await self._repository.get_by_id(
            complaint_id,
            with_lock=True,
        )

        now = now or datetime.now(timezone.utc)

        complaint.status = status
        complaint.updated_at = now

        if status == ComplaintStatus.RESPONDED:
            complaint.responded_at = now

        return await self._repository.save(
            complaint,
            flush=True,
        )
