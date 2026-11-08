from app.features.products.variant_size.variant_size_repository import (
    VariantSizeRepository,
)
from app.features.products.labels.dto import LabelDTO


class LabelService:

    def __init__(
        self,
        variant_size_repository: VariantSizeRepository,
    ):
        self.variant_size_repository = variant_size_repository


    async def get_label(
        self,
        variant_size_id: int,
    ) -> LabelDTO:

        label = await self.variant_size_repository.get_label(
            variant_size_id
        )

        return label


    async def get_many_labels(
        self,
        variant_size_ids: list[int],
    ) -> list[LabelDTO]:

        labels = await self.variant_size_repository.get_many_labels(
            variant_size_ids
        )

        return labels