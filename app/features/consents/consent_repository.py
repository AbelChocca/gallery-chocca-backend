from uuid import UUID

from sqlalchemy import select

from app.features.consents.types import ConsentType
from app.features.consents.user_consent_entity import (
    UserConsentEntity,
)
from app.features.consents.models.user_consent import (
    UserConsentTable,
)
from app.infra.db.repositories.base_repository import (
    BaseRepository,
)


class UserConsentRepository(
    BaseRepository[UserConsentEntity, UserConsentTable]
):
    async def get_latest_by_owner(
        self,
        *,
        user_id: int | None,
        session_id: UUID | None,
        consent_type: ConsentType,
    ) -> UserConsentEntity | None:

        if user_id is not None:
            owner_condition = (
                UserConsentTable.user_id == user_id
            )
        elif session_id is not None:
            owner_condition = (
                UserConsentTable.session_id == session_id
            )
        else:
            return None

        stmt = (
            select(UserConsentTable)
            .where(
                UserConsentTable.consent_type == consent_type,
                owner_condition,
            )
            .order_by(
                UserConsentTable.created_at.desc(),
                UserConsentTable.id.desc(),
            )
            .limit(1)
        )

        result = await self._db_session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._base_mapper.to_entity(model)