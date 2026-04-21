from app.infra.db.repositories.sqlmodel_product_repository import PostgresProductRepository
from app.infra.db.repositories.sqlmodel_image_repository import PostgresImageRepository
from app.infra.db.repositories.sqlmodel_favorites_repository import PostgresFavoritesRepository
from app.domain.product.dto.product_dto import PublishProductCommand
from app.shared.services.slug.protocol import SlugProtocol
from app.domain.product.entities.product import Product
from app.domain.media.entities.image import ImageEntity
from app.infra.saga_service import SagaService
from app.infra.cache.protocole import CacheProtocol
from app.domain.media.media_dto import MediaImageDTO
from app.domain.product.dto.product_dto import UpdateProductCommand, FilterProductCommand
from app.shared.services.cache_strategy.cache_strategy_service import CacheStrategyService
from app.shared.services.pagination.pagination_service import PaginationService
from app.core.exceptions import ValidationError

from typing import List, BinaryIO, Dict, Callable, Any
from collections import defaultdict

class ProductService:
    def __init__(
            self,
            product_repo: PostgresProductRepository,
            favorite_repo: PostgresFavoritesRepository,
            cache_service: CacheProtocol,
            cache_strategy_service: CacheStrategyService,
            pagination_service: PaginationService,
            image_repo: PostgresImageRepository,
            slug_service: SlugProtocol
        ):
        self._product_repo: PostgresProductRepository = product_repo
        self._favorite_repo: PostgresFavoritesRepository = favorite_repo
        self._image_repo: PostgresImageRepository = image_repo
        self._slug_service: SlugProtocol = slug_service
        self._cache_service: CacheProtocol = cache_service
        self._cache_strategy_service: CacheStrategyService = cache_strategy_service
        self._pagination_service: PaginationService = pagination_service
    
    async def get_product_by_id(
            self,
            product_id: int
    ) -> dict[str, Any]:
        cache_args = self._cache_strategy_service.operation_by_id(name="product", entity_id=product_id)
        ttl: int = self._cache_strategy_service.determinate_ttl(cache_args)
        product_key: str = self._cache_strategy_service.generate_key(cache_args)

        return await self._cache_service.get_or_set_with_lock(
            key=product_key,
            ttl=ttl,
            callback=self._get_product_data,
            kwargs={
                "product_id": product_id
            }
        )
    
    async def upload_images_by_temp_key(
            self, 
            saga_service: SagaService,
            images_file: List[BinaryIO],
            temp_keys: List[str],
            action_func: Callable[..., Any],
            compesantion_func: Callable[..., Any]
        ) -> Dict[str, List[ImageEntity]]:
        images_per_temp_key = self._map_images_by_temp_key(images_file, temp_keys)
        result: Dict[str, List[ImageEntity]] = defaultdict(list)

        for temp_key, images_bin in images_per_temp_key.items():
            saga_service.add_step(
                action=action_func,
                action_name="upload_images_batch",
                action_kwargs={
                    "images_resource": images_bin,
                    "folder": "products"
                }
            )

            images: List[MediaImageDTO] = await saga_service.execute_last()

            saga_service.set_last_step_compensation(
                compesation=compesantion_func,
                compensation_name="move_images_to_trash",
                compensation_kwargs={
                    "images_public_id": [image.public_id for image in images]
                }
            )

            result[temp_key] = [
                ImageEntity(
                    image_url=image.url,
                    owner_type="variant",
                    public_id=image.public_id
                )
                for image in images
            ]
        return result
    
    async def delete_existing_entities(self, command: UpdateProductCommand) -> list[str]:
        images_public_id_to_delete = []
        for variant in command.variants:
            if variant.id is None: continue

            if variant.to_delete:
                images_public_id_to_delete.extend(
                    image.public_id
                    for image in (variant.imagenes or [])
                    if image.public_id is not None
                )
            else:
                images_public_id_to_delete.extend(
                    image.public_id
                    for image in (variant.imagenes or None)
                    if image.to_delete and image.public_id is not None
                )

        self._validate_the_deleting(command)

        await self._image_repo.delete_many_images_by_publics_id("variant", images_public_id_to_delete)

        return images_public_id_to_delete
    
    async def create_product_with_variants(
            self, 
            product: PublishProductCommand,
            images_by_temp_key: Dict[str, List[ImageEntity]]
    ) -> Product:
        new_product = Product(
            nombre=product.nombre,
            descripcion=product.descripcion,
            marca=product.marca,
            categoria=product.categoria,
            model_family=product.model_family,
            fit=product.fit,
            variants=[],
            slug=self._slug_service.generate(product.nombre),
        )

        for variant in product.variants:
            new_product.add_variant(
                variant_command=variant,
                images=images_by_temp_key[variant.temp_key]
            )

        product_db = await self._product_repo.save(new_product)

        self._sync_variant_images(new_product, product_db)

        await self._image_repo.save_many(product_db.all_variant_images)

        # Invalidating cache
        await self._invalidate_products()

        return product_db
    
    async def update_product_with_variants(
        self,
        product_id: int,
        command: UpdateProductCommand,
        images_by_temp_key: Dict[str, List[ImageEntity]] | None = None
    ) -> Product:
        images_by_temp_key = images_by_temp_key or {}

        product = await self.get_product_entity_by_id(product_id)

        product.sync_existing_variants(command.variants)

        if command.name_changed:
            new_slug = self._slug_service.generate(command.nombre)
            product.slug = new_slug

        product.update_product(command.to_dict)    

        for variant in command.variants:
            temp_key = variant.temp_key
            images: list[ImageEntity] = images_by_temp_key.get(temp_key, [])

            if temp_key.startswith("temp"):
                product.add_variant(
                    color=variant.color,
                    sizes=[variant_size.size for variant_size in variant.sizes if variant_size is not None],
                    images=images
                )
            elif temp_key.startswith("db"):
                _, variant_id = temp_key.split(":")
                variant_id = int(variant_id)

                for image in images:
                    product.add_image_on_existing_variant(
                        variant_id=variant_id,
                        image_url=image.image_url,
                        service_id=image.public_id
                )
                    
        new_product = await self._product_repo.save(product)
        if product.has_new_images:
            self._sync_variant_images(product, new_product)

            await self._image_repo.save_many(new_product.images_without_id)

        await self._invalidate_product(product.id)

        await self._invalidate_products()
    
    async def get_products_related(self, query: str, limit: int) -> list[Product]:
        products = await self._product_repo.search_related(query, 0, limit)

        return await self.enrich_products(products)
    
    async def get_products(
        self,
        command: FilterProductCommand,
        page: int = 1,
        limit: int = 20,
    ) -> dict[str, Any]:
        cache_args = self._cache_strategy_service.operation_list(name="product", values={ "filters": command.to_dict, "page": page, "limit": limit})
        ttl: int = self._cache_strategy_service.determinate_ttl(cache_args)
        products_key: str = self._cache_strategy_service.generate_key(cache_args)
        offset = self._pagination_service.get_offset(page, limit)

        return await self._cache_service.get_or_set_with_lock(
            key=products_key,
            ttl=ttl,
            callback=self._get_products_data,
            kwargs={
                "command": command,
                "offset": offset,
                "limit": limit
            }
        )
    
    async def delete_product(
            self,
            product_id: int,
            saga_service: SagaService,
            action_func: Callable[..., Any],
            compesantion_func: Callable[..., Any]
    ) -> None:
        product_to_delete: Product = await self.get_product_entity_by_id(product_id)

        # Del images from cloud service
        images_to_delete: List[str] = product_to_delete.all_image_public_ids

        saga_service.add_step(
            action=action_func,
            action_name=action_func.__name__,
            compensation=compesantion_func,
            compensation_name=compesantion_func.__name__,
            action_kwargs={
                "images_public_id": images_to_delete
            },
            compensation_kwargs={
                "images_public_id": images_to_delete
            }
        )

        await self._image_repo.delete_many_images_by_owners_id("variant", product_to_delete.variant_ids)

        await self._favorite_repo.delete_favorite_of_product(product_id)

        await self._product_repo.delete_by_id(product_id)

        await self._invalidate_product(product_id)
        await self._invalidate_products()

    async def enrich_products(
        self,
        products: list[Product]
    ) -> list[Product]:
        variants_id: List[int] = []
        for product in products:
            variants_id.extend(product.variant_ids)

        images_by_owner_id = await self._get_images_by_variant_ids(variants_id)

        for product in products:
            product.sync_images_to_variants(images_by_owner_id)
        
        return products
    
    async def enrich_product(
            self,
            product: Product
    ) -> Product:
        variants_id: List[int] = product.variant_ids

        images_by_owner_id = await self._get_images_by_variant_ids(variants_id)

        product.sync_images_to_variants(images_by_owner_id)

        return product
    
    async def get_product_entity_by_id(
            self,
            product_id: int
    ) -> Product:
        product = await self.enrich_product(
                await self._product_repo.get_by_id(product_id)
            )

        return product
    
    def validate_product_form(
        self,
        images_file: List[BinaryIO],
        command: PublishProductCommand | UpdateProductCommand
    ) -> None:
        colors = [v.color for v in command.variants]
        if images_file is not None and command.temp_keys is not None and len(images_file) != len(command.temp_keys):
            raise ValidationError(
                "Length of image list and his temp's id aren't match",
                {
                    "event": "create_product_case/_validate",
                    "image_file_sample": images_file[:5],
                    "temp_keys_sample": command.temp_keys[:5]
                }
            )
        
        if len(colors) != len(set(colors)):
            raise ValidationError(
                "Product can't have repeated colors.",
                {
                    "event": "create_product_case/_validate"
                }
            )
        
        for variant in command.variants:
            sizes = [s.size for s in variant.sizes if s.size is not None]
            if len(sizes) != len(set(sizes)):
                raise ValidationError(
                    "Product variant can't have repeated sizes.",
                    {
                        "event": "create_product_case/_validate"
                    }
                )

            has_number_size = any(s.isdigit() for s in sizes)
            has_alpha_size  = any(not s.isdigit() for s in sizes)

            if has_number_size and has_alpha_size:
                raise ValidationError(
                    "Sizes cannot mix numeric and alphabetic values",
                    {
                        "event": "create_product_case/_validate"
                    }
                )
            
    async def count_products(
        self,
        command: FilterProductCommand | None = None
    ) -> int:
        res = await self._product_repo.count_filtered_products(command)
        return res
    
    async def count_by_category(self) -> list[dict[str, Any]]:
        res = await self._product_repo.get_count_by_category()

        return [
            {
                "category": category,
                "total": total
            }
            for category, total in res
        ]
    
    async def get_last_n(self, n: int) -> list[Product]:
        last_n_products = await self._product_repo.get_last_n_products(n)

        enriched_products = await self.enrich_products(last_n_products)

        return [
            product.to_dict
            for product in enriched_products
        ]
    
    def _validate_the_deleting(
            self,
            product_command: UpdateProductCommand
            ) -> None:
        new_images_per_variant = product_command.new_images_per_variant if product_command.has_new_images else {}

        current_variants_count = product_command.existing_variants_count
        variants_to_delete_count = product_command.variants_to_delete
        new_variants_count = product_command.new_variants_count

        diff: int = current_variants_count - variants_to_delete_count + new_variants_count
        if diff < 1:
            raise ValidationError(
                "Product must be at least one variant",
                {
                    "entity": "Product",
                    "event": "raise_cannot_delete_variants",
                    "current_variants_count": current_variants_count,
                    "variants_to_delete_count": variants_to_delete_count,
                    "new_variants_count": new_variants_count
                }
            )
        
        for variant in product_command.variants:
            if variant.id is not None and variant.to_delete: continue

            current_images_count = variant.existing_images_count
            images_to_delete_count = variant.images_to_delete_count
            new_images_count = new_images_per_variant.get(variant.temp_key, 0)

            diff: int = current_images_count - images_to_delete_count + new_images_count

            if diff < 1:
                raise ValidationError(
                    "Variant must be at least one image, cannot delete",
                    {
                        "entity": "ProductVariant",
                        "event": "raise_cannot_delete_image",
                        "variant_id": variant.id,
                        "existing_images_count": current_images_count,
                        "images_to_delete_count": images_to_delete_count,
                        "new_images_count": new_images_count
                    }
                    )
            
            current_sizes_count = variant.existing_sizes_count
            sizes_to_delete_count = variant.sizes_to_delete_count
            new_sizes_count = variant.new_sizes_count

            diff: int = current_sizes_count - sizes_to_delete_count + new_sizes_count

            if diff < 1:
                raise ValidationError(
                    "Variant must be at least one size, cannot delete.",
                    {   
                        "entity": "ProductVariant",
                        "event": "raise_cannot_delete_size",
                        "variant_id": variant.id,
                        "current_sizes_count": current_sizes_count,
                        "sizes_to_delete_count": sizes_to_delete_count,
                        "new_sizes_count": new_sizes_count
                    }
                )


    async def _get_products_data(
        self,
        command: FilterProductCommand,
        offset: int = 0,
        limit: int = 20,
    ) -> dict[str, Any]:
        num_products = await self.count_products(command)

        total_pages = self._pagination_service.get_total_pages(num_products, limit)
        current_page = self._pagination_service.get_current_page(offset, limit)
        
        products = await self._product_repo.get_all(command, offset, limit)
        await self.enrich_products(products)

        return {
            "pagination": {
                "total_pages": total_pages,
                "current_page": current_page
            },
            "products": [
                product.to_dict
                for product in products
            ],
            "total_items": num_products
        }
    
    async def _get_product_data(
        self,
        product_id: int
    ) -> dict[str, Any]:
        product = await self.enrich_product(
            await self._product_repo.get_by_id(product_id)
        )

        return product.to_dict
        
    async def _invalidate_products(self) -> None:
        args = self._cache_strategy_service.operation_list("product", {})
        key = self._cache_strategy_service.generate_family_key(args)
        await self._cache_service.invalidate_family(key)

    async def _invalidate_product(self, product_id: int) -> None:
        args = self._cache_strategy_service.operation_by_id("product", product_id)
        key: str = self._cache_strategy_service.generate_key(args)
        await self._cache_service.cache_delete(key)

    def _sync_variant_images(self, source_product: Product, target_product: Product) -> None:
        """
        Sincroniza las imágenes de las variantes de source_product hacia target_product.
        """
        variant_per_color = {variant.color: variant for variant in source_product.variants}
        for new_variant in target_product.variants:
            prev_variant = variant_per_color.get(new_variant.color)
            if not prev_variant:
                continue
            new_variant.imagenes = prev_variant.imagenes.copy()

    def _map_images_by_temp_key(
        self,
        images_file: List[BinaryIO], 
        temp_keys: List[str]
    ) -> Dict[str, List[BinaryIO]]:
        images_per_temp_key: Dict[str, List[BinaryIO]] = defaultdict(list)
        for file, temp_key in zip(images_file, temp_keys):
            images_per_temp_key[temp_key].append(file)
        return images_per_temp_key
    
    def _group_images_by_owner(self, images: list[ImageEntity]):
        images_by_owner_id = defaultdict(list)
        for image in images:
            images_by_owner_id[image.owner_id].append(image)
        return images_by_owner_id
    
    async def _get_images_by_variant_ids(self, variant_ids: list[int]):
        images = await self._image_repo.get_by_owners(
            owner_type="variant",
            owner_ids=variant_ids
        )
        return self._group_images_by_owner(images)