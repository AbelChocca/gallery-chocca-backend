from sqlalchemy import select, func, or_

from app.infra.db.repositories.base_repository import (
    BaseRepository,
)

from app.features.complaints.entities.complaint import Complaint
from app.features.complaints.models.complaint import (
    ComplaintTable,
    complaint_number_sequence,
)
from app.features.complaints.types.complaint import (
    AdminComplaintListItemDTO,
    ComplaintFilters,
)


class ComplaintRepository(
    BaseRepository[Complaint, ComplaintTable]
):

    async def next_complaint_sequence(self) -> int:
        result = await self._db_session.execute(
            select(complaint_number_sequence.next_value())
        )
        return int(result.scalar_one())

    async def get_by_complaint_number(
        self,
        complaint_number: str,
    ) -> Complaint | None:
        statement = select(ComplaintTable).where(
            ComplaintTable.complaint_number == complaint_number
        )

        result = await self._db_session.execute(statement)
        model = result.scalar_one_or_none()

        return (
            self._base_mapper.to_entity(model)
            if model is not None
            else None
        )

    async def get_by_public_id(
        self,
        public_id,
    ) -> Complaint | None:
        statement = select(ComplaintTable).where(
            ComplaintTable.public_id == public_id
        )

        result = await self._db_session.execute(statement)
        model = result.scalar_one_or_none()

        return (
            self._base_mapper.to_entity(model)
            if model is not None
            else None
        )

    
    async def get_admin_complaints(
        self,
        *,
        filters: ComplaintFilters,
        offset: int,
        limit: int,
    ) -> tuple[list[AdminComplaintListItemDTO], int]:

        conditions = []

        if filters.status is not None:
            conditions.append(
                ComplaintTable.status == filters.status
            )

        if filters.complaint_type is not None:
            conditions.append(
                ComplaintTable.complaint_type == filters.complaint_type
            )

        if filters.created_at_from is not None:
            conditions.append(
                ComplaintTable.created_at >= filters.created_at_from
            )

        if filters.created_at_to is not None:
            conditions.append(
                ComplaintTable.created_at <= filters.created_at_to
            )

        if filters.search:
            search_pattern = f"%{filters.search.strip()}%"

            conditions.append(
                or_(
                    ComplaintTable.complaint_number.ilike(
                        search_pattern
                    ),
                    ComplaintTable.first_name.ilike(
                        search_pattern
                    ),
                    ComplaintTable.last_name.ilike(
                        search_pattern
                    ),
                    func.concat(
                        ComplaintTable.first_name,
                        " ",
                        ComplaintTable.last_name,
                    ).ilike(search_pattern),
                )
            )

        count_query = (
            select(func.count(ComplaintTable.id))
            .where(*conditions)
        )

        total_items = (
            await self._db_session.scalar(count_query)
        ) or 0

        statement = (
            select(
                ComplaintTable.id,
                ComplaintTable.complaint_number,
                ComplaintTable.first_name,
                ComplaintTable.last_name,
                ComplaintTable.complaint_type,
                ComplaintTable.status,
                ComplaintTable.response_channel,
                ComplaintTable.created_at,
                ComplaintTable.response_due_at,
                ComplaintTable.responded_at,
            )
            .where(*conditions)
            .order_by(
                ComplaintTable.created_at.desc(),
                ComplaintTable.id.desc(),
            )
            .offset(offset)
            .limit(limit)
        )

        result = await self._db_session.execute(statement)

        items = [
            AdminComplaintListItemDTO(
                id=row.id,
                complaint_number=row.complaint_number,
                customer_name=(
                    f"{row.first_name} {row.last_name}"
                ).strip(),
                complaint_type=row.complaint_type,
                status=row.status,
                response_channel=row.response_channel,
                created_at=row.created_at,
                response_due_at=row.response_due_at,
                responded_at=row.responded_at,
            )
            for row in result.all()
        ]

        return items, total_items
