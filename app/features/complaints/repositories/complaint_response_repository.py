
from sqlalchemy import select

from app.infra.db.repositories.base_repository import (
    BaseRepository,
)

from app.features.complaints.entities.complaint_response import (
    ComplaintResponse,
)
from app.features.complaints.models.complaint_response import (
    ComplaintResponseTable,
)

class ComplaintResponseRepository(
    BaseRepository[ComplaintResponse, ComplaintResponseTable]
):

    async def get_by_complaint_id(
        self,
        complaint_id: int,
    ) -> list[ComplaintResponse]:
        statement = (
            select(ComplaintResponseTable)
            .where(
                ComplaintResponseTable.complaint_id == complaint_id
            )
            .order_by(
                ComplaintResponseTable.created_at.asc(),
                ComplaintResponseTable.id.asc(),
            )
        )

        result = await self._db_session.execute(statement)

        return [
            self._base_mapper.to_entity(model)
            for model in result.scalars().all()
        ]