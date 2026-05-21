from app.infra.db.repositories.sqlmodel_product_repository import PostgresProductRepository
from app.infra.db.repositories.sqlmodel_image_repository import PostgresImageRepository
from app.infra.db.repositories.sqlmodel_favorites_repository import PostgresFavoritesRepository
from app.features.products.dto.product_dto import PublishProductCommand, CreateProductResponse
from app.shared.slug.protocol import SlugProtocol
from app.features.products.entities.product import Product
from app.features.media.entities.image import ImageEntity
from app.infra.saga_service import SagaService
from app.infra.cache.protocole import CacheProtocol
from app.features.products.dto.product_dto import UpdateProductCommand, FilterProductCommand
from app.shared.pagination.pagination_service import PaginationService
from app.core.exceptions import ValidationError
from app.features.products.types import ProductsOverview, CountProductPerCategory
from app.infra.saga_service import SagaService
from app.features.media.service import MediaService
from app.core.app_exception import AppException

from typing import List, BinaryIO, Dict, Callable, Any
from collections import defaultdict

class ProductService:
    def __init__(
            self,
            product_repo: PostgresProductRepository,
            favorite_repo: PostgresFavoritesRepository,
            saga_service: SagaService,
            cache_service: CacheProtocol,
            pagination_service: PaginationService,
            image_repo: PostgresImageRepository,
            slug_service: SlugProtocol,
            media_service: MediaService,
        ):
        self._product_repo: PostgresProductRepository = product_repo
        self._favorite_repo: PostgresFavoritesRepository = favorite_repo
        self._image_repo: PostgresImageRepository = image_repo
        self._saga_service: SagaService = saga_service
        self._slug_service: SlugProtocol = slug_service
        self._cache_service: CacheProtocol = cache_service
        self._pagination_service: PaginationService = pagination_service
        self._media_service: MediaService = media_service
    
    async def get_product_by_id(
            self,
            product_id: int
    ) -> dict[str, Any]:
        return await self._cache_service.get_or_set_with_lock(
            tag="product",
            callback=self._get_product_data,
            kwargs={
                "product_id": product_id
            },
            key_args={
                "entity_id": product_id
            }
        )
    
    async def delete_existing_entities(self, command: UpdateProductCommand) -> None:
        self._validate_the_deleting(command)

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
                    for image in (variant.imagenes or [])
                    if image.to_delete and image.public_id is not None
                )

        await self._media_service.delete_images(
            owner_type="variant",
            images_public_id=images_public_id_to_delete,
            saga_service=self._saga_service
        )

        await self._saga_service.execute_last()
    
    async def create_product_with_variants(
            self, 
            images_file: List[BinaryIO],
            command: PublishProductCommand,
    ) -> dict:
        try:
            self._validate_product_form(images_file, command)

            new_product = Product(
                nombre=command.nombre,
                descripcion=command.descripcion,
                marca=command.marca,
                categoria=command.categoria,
                model_family=command.model_family,
                fit=command.fit,
                variants=[],
                slug=self._slug_service.generate(command.nombre),
            )

            for variant in command.variants:
                new_product.add_variant(
                    variant_command=variant
                )

            product_db = await self._product_repo.save(new_product)

            images_per_color = self._map_images_by_color(images_file, command)

            for variant in product_db.variants:
                images = images_per_color.get(variant.color)

                await self._media_service.create_image_batch(
                    image_resources=images,
                    folder="products",
                    owner_type="variant",
                    owner_id=variant.id,
                    saga_service=self._saga_service
                )

            # Invalidating cache
            await self._cache_service.invalidate_entities("product")

            return {
                "id": product_db.id, 
                "slug": product_db.slug
            }
        except AppException as ae:
            await self._saga_service.compensate_all()

            ae.context["compensation_errors"] = self._saga_service.compensation_errors

            raise ae
    
    async def update_product_with_variants(
        self,
        product_id: int,
        command: UpdateProductCommand,
        new_images_file: List[BinaryIO] | None = None
    ) -> Product:
        if command.has_all_variants_deleted:
            raise ValidationError(
                "Product need at least one variant",
                {
                    "event": "update_product_case/execute",
                    "product_id": product_id
                }
            )
        self._validate_product_form(new_images_file, command)

        try:
            await self.delete_existing_entities(command)
            
            product = await self.get_product_entity_by_id(product_id)
            product.sync_existing_variants(command.variants)

            if command.name_changed:
                new_slug = self._slug_service.generate(command.nombre)
                product.slug = new_slug

            product.update_product(command.to_dict)    

            for variant in command.new_variants:
                product.add_variant(
                    color=variant.color,
                    sizes=[variant_size.size for variant_size in variant.sizes if variant_size is not None],
                )
                        
            new_product = await self._product_repo.save(product)

            images_per_color = self._map_images_by_color(new_images_file, command)

            if command.has_new_images:
                for variant in new_product.variants:
                    images = images_per_color.get(variant.color)

                    await self._media_service.create_image_batch(
                        image_resources=images,
                        folder="products",
                        owner_id=variant.id,
                        owner_type="variant",
                        saga_service=self._saga_service
                    )

            await self._cache_service.invalidate_entity("product", product_id)

            await self._cache_service.invalidate_entities("product")
        except AppException as ae:
            await self._saga_service.compensate_all()

            ae.context["compensation_errors"] = self._saga_service.compensation_errors

            raise ae
    
    async def get_products_related(self, query: str, limit: int) -> list[dict]:
        products = await self._product_repo.search_related(query, 0, limit)

        enriched_products = await self.enrich_products(products)

        return [
            product.to_dict
            for product in enriched_products
        ]
    
    async def get_products(
        self,
        command: FilterProductCommand,
        page: int = 1,
        limit: int = 20,
    ) -> dict[str, Any]:
        offset = self._pagination_service.get_offset(page, limit)

        return await self._cache_service.get_or_set_with_lock(
            tag="product",
            callback=self._get_products_data,
            kwargs={
                "command": command,
                "offset": offset,
                "limit": limit
            },
            key_args={
                "filters": command.to_dict, 
                "page": page, 
                "limit": limit
            }
        )
    
    async def delete_product(
            self,
            product_id: int
    ) -> None:
        product_to_delete: Product = await self.get_product_entity_by_id(product_id)

        try:
            await self._media_service.delete_images(
                owner_type="variant",
                images_public_id=product_to_delete.all_image_public_ids,
                saga_service=self._saga_service
            )

            await self._favorite_repo.delete_favorite_of_product(product_id)

            await self._product_repo.delete_by_id(product_id)

            await self._cache_service.invalidate_entity("product", product_id)
            await self._cache_service.invalidate_entities("product")

            await self._saga_service.execute_all()
        except AppException as ae:
            await self._saga_service.compensate_all()

            if self._saga_service.compensation_errors:
                ae.context["compensation_errors"] = (
                    self._saga_service.compensation_errors
                )

            raise ae

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
    
    async def overview(
        self
    ) -> ProductsOverview:
        total_products = await self._count_products()
        products_per_category = await self._count_by_category()
        last_three = await self._get_last_n(3)

        overview_res: ProductsOverview = {
            "total_products": total_products,
            "products_per_category": products_per_category,
            "last_n_products": last_three
        }

        return overview_res
    
    def _validate_product_form(
        self,
        images_file: List[BinaryIO],
        command: PublishProductCommand | UpdateProductCommand
    ) -> None:
        colors = [v.color for v in command.variants]
        if images_file is not None and command.temp_keys is not None and len(images_file) != len(command.temp_keys):
            raise ValidationError(
                "Length of image list and his temp's id aren't match",
                {
                    "event": "product_service/_validate_form",
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
            
    async def _count_products(
        self,
        command: FilterProductCommand | None = None
    ) -> int:
        res = await self._product_repo.count_filtered_products(command)
        return res
    
    async def _count_by_category(self) -> list[CountProductPerCategory]:
        res = await self._product_repo.get_count_by_category()

        products_per_category: list[CountProductPerCategory] = [
            {
                "total": total,
                "category": category
            }
            for category, total in res
        ]

        return products_per_category
    
    async def _get_last_n(self, n: int) -> list[dict]:
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
        num_products = await self._count_products(command)

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

    def _map_images_by_color(
        self,
        images_file: List[BinaryIO] | None = None, 
        command: PublishProductCommand | UpdateProductCommand | None = None,
    ) -> Dict[str, List[BinaryIO]]:
        if images_file is None and command is None:
            return
        
        images_per_temp_key: Dict[str, List[BinaryIO]] = defaultdict(list)
        for file, temp_key in zip(images_file, command.temp_keys or []):
            images_per_temp_key[temp_key].append(file)

        images_per_color: dict[str, list[BinaryIO]] = defaultdict(list)

        for variant in command.variants:
            images = images_per_temp_key.get(variant.temp_key, [])
            images_per_color[variant.color] = images

        return images_per_color
    
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