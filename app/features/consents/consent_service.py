from uuid import UUID

from app.features.consents.types import (
    CookiePreferencesDTO,
    ConsentDTO,
    ConsentSummaryDTO,
    ConsentType
)
from app.features.consents.user_consent_entity import (
    UserConsentEntity,
)
from app.features.consents.consent_repository import (
    UserConsentRepository,
)
from app.features.consents.config.policy_versions import (
    POLICY_VERSIONS,
)


class ConsentService:
    def __init__(
        self,
        consent_repository: UserConsentRepository,
    ):
        self.consent_repository = consent_repository

    @staticmethod
    def _to_dto(
        entity: UserConsentEntity,
    ) -> ConsentDTO:
        if entity.id is None:
            raise ValueError("Consent has no persisted ID")

        return ConsentDTO(
            id=entity.id,
            consent_type=entity.consent_type,
            version=entity.version,
            accepted=entity.accepted,
            preferences=entity.preferences,
            created_at=entity.created_at,
        )

    async def get_latest(
        self,
        *,
        user_id: int | None,
        session_id: UUID | None,
        consent_type: ConsentType,
    ) -> ConsentDTO | None:
        entity = await self.consent_repository.get_latest_by_owner(
            user_id=user_id,
            session_id=session_id,
            consent_type=consent_type,
        )

        if entity is None:
            return None

        return self._to_dto(entity)

    async def get_summary(
        self,
        *,
        user_id: int | None,
        session_id: UUID | None,
    ) -> ConsentSummaryDTO:
        cookies = await self.get_latest(
            user_id=user_id,
            session_id=session_id,
            consent_type=ConsentType.COOKIES,
        )

        terms = await self.get_latest(
            user_id=user_id,
            session_id=session_id,
            consent_type=ConsentType.TERMS,
        )

        return ConsentSummaryDTO(
            cookies=cookies,
            terms=terms,
        )

    async def save_cookies(
        self,
        *,
        user_id: int | None,
        session_id: UUID | None,
        preferences: CookiePreferencesDTO,
    ) -> ConsentDTO:
        latest = await self.consent_repository.get_latest_by_owner(
            user_id=user_id,
            session_id=session_id,
            consent_type=ConsentType.COOKIES,
        )

        values = {
            "analytics": preferences.analytics,
            "marketing": preferences.marketing,
        }

        if (
            latest is not None
            and latest.version == POLICY_VERSIONS.cookies
            and latest.preferences == values
        ):
            return self._to_dto(latest)

        entity = UserConsentEntity(
            user_id=user_id if user_id is not None else None,
            session_id=(
                None if user_id is not None else session_id
            ),
            consent_type=ConsentType.COOKIES,
            version=POLICY_VERSIONS.cookies,
            accepted=any(values.values()),
            preferences=values,
        )

        saved = await self.consent_repository.save(entity)
        
        return self._to_dto(saved)

    async def accept_terms(
        self,
        *,
        user_id: int | None,
        session_id: UUID | None,
    ) -> ConsentDTO:
        latest = await self.consent_repository.get_latest_by_owner(
            user_id=user_id,
            session_id=session_id,
            consent_type=ConsentType.TERMS,
        )

        if (
            latest is not None
            and latest.version == POLICY_VERSIONS.terms
            and latest.accepted
        ):
            return self._to_dto(latest)

        entity = UserConsentEntity(
            user_id=user_id if user_id is not None else None,
            session_id=(
                None if user_id is not None else session_id
            ),
            consent_type=ConsentType.TERMS,
            version=POLICY_VERSIONS.terms,
            accepted=True,
            preferences=None,
        )

        saved = await self.consent_repository.save(entity)

        return self._to_dto(saved)