from app.features.favorites.service import FavoriteService
from app.features.media.service import MediaService
from app.features.products.constants import PRODUCT_CACHE_KEY_TAG
from app.features.products.service import ProductService
from app.infra.cache.redis_service import RedisService
from app.infra.saga.saga_service import SagaService
from app.features.cart.service import CartService
from app.infra.saga.saga_use_case import UseCaseSaga


class DeleteProductUseCase(UseCaseSaga):

    def __init__(
        self,
        saga_service: SagaService,
        product_service: ProductService,
        media_service: MediaService,
        favorite_service: FavoriteService,
        cart_service: CartService,
        cache_service: RedisService,
    ):
        super().__init__(saga_service)

        self._cart_service = cart_service
        self._product_service = product_service
        self._media_service = media_service
        self._favorite_service = favorite_service
        self._cache_service = cache_service

    async def execute(
        self,
        product_id: int,
    ) -> None:

        async def operation():

            product = await self._product_service.get_product_entity_by_id(
                product_id
            )

            await self._favorite_service.delete_favorite_of_product(
                product_id
            )

            await self._product_service.delete_product(
                product_id
            )

            await self._cart_service.delete_product_from_carts(
                product_id
            )

            await self._media_service.delete_images(
                owner_type="variant",
                images_public_id=product.all_image_public_ids
            )

            await self._saga.execute_step(
                action=self._media_service.move_images_to_trash,
                action_kwargs={
                    "images_public_id": product.all_image_public_ids
                },
                compensation_factory=lambda _: (
                    self._media_service.recover_images_from_trash,
                    self._media_service.recover_images_from_trash.__name__,
                    {
                        "images_public_id": product.all_image_public_ids
                    }
                )
            )

            await self._cache_service.invalidate_entity(
                PRODUCT_CACHE_KEY_TAG,
                product_id
            )

            await self._cache_service.invalidate_entities(
                PRODUCT_CACHE_KEY_TAG
            )

        await self._saga.execute_safely(operation)