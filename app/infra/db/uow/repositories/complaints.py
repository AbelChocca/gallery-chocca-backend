
from app.features.complaints.repositories.complaint_repository import (
    ComplaintRepository,
)
from app.features.complaints.repositories.complaint_response_repository import (
    ComplaintResponseRepository,
)

from app.features.complaints.models.complaint import (
    ComplaintTable,
)
from app.features.complaints.models.complaint_response import (
    ComplaintResponseTable,
)

from app.features.complaints.mappers.complaint_mapper import (
    ComplaintMapper,
)
from app.features.complaints.mappers.complaint_response_mapper import (
    ComplaintResponseMapper,
)


class ComplaintsRepositoriesMixin:

    @property
    def complaints(self) -> ComplaintRepository:
        return self._get_or_create(
            "complaints",
            lambda: ComplaintRepository(
                self.session,
                ComplaintMapper,
                ComplaintTable,
            ),
        )

    @property
    def complaint_responses(self) -> ComplaintResponseRepository:
        return self._get_or_create(
            "complaint_responses",
            lambda: ComplaintResponseRepository(
                self.session,
                ComplaintResponseMapper,
                ComplaintResponseTable,
            ),
        )
