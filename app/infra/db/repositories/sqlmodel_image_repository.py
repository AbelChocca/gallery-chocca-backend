from app.infra.db.repositories.base_repository import BaseRepository
from app.infra.db.models.model_media import MediaImageTable
from app.domain.media.entities.image import ImageEntity

from sqlmodel import select, col

from typing import List

class PostgresImageRepository(BaseRepository[ImageEntity, MediaImageTable]):
    async def get_images_from_variants_id(self, variants_id: List[int]) -> List[ImageEntity]:
        statement = (
            select(MediaImageTable)
            .where(MediaImageTable.owner_type == "product_variant")
            .where(col(MediaImageTable.owner_id).in_(variants_id))
        )

        res: List[MediaImageTable] = (await self._db_session.exec(statement)).all()

        return [
            self._base_mapper.to_entity(image_table)
            for image_table in res
        ]