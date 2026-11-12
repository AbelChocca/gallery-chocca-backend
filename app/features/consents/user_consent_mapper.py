from app.features.consents.user_consent_entity import (
    UserConsentEntity,
)
from app.features.consents.models.user_consent import (
    UserConsentTable,
)
from app.infra.db.mappers.base_mapper import BaseMapper


class UserConsentMapper(
    BaseMapper[UserConsentEntity, UserConsentTable]
):
    @staticmethod
    def to_entity(
        model: UserConsentTable,
    ) -> UserConsentEntity:
        return UserConsentEntity(
            id=model.id,
            user_id=model.user_id,
            session_id=model.session_id,
            consent_type=model.consent_type,
            version=model.version,
            accepted=model.accepted,
            preferences=model.preferences,
            created_at=model.created_at,
        )

    @staticmethod
    def to_db_model(
        entity: UserConsentEntity,
        existing_model: UserConsentTable | None = None,
    ) -> UserConsentTable:
        model = existing_model or UserConsentTable()

        model.id = entity.id
        model.user_id = entity.user_id
        model.session_id = entity.session_id
        model.consent_type = entity.consent_type
        model.version = entity.version
        model.accepted = entity.accepted
        model.preferences = entity.preferences
        model.created_at = entity.created_at

        return model