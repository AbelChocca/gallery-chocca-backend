from datetime import datetime, timezone

from app.core.exceptions import ValueNotFound

from app.features.pricing.entities.coupon import Coupon
from app.features.pricing.entities.coupon_redemption import (
    CouponRedemption,
)

from app.features.pricing.repositories.coupon_repsitory import (
    CouponRepository,
)

from app.features.pricing.repositories.coupon_redemption_repository import (
    CouponRedemptionRepository,
)
from app.features.pricing.resolvers.coupon_resolver import CouponResolver
from app.shared.pagination.pagination_service import (
    PaginationService,
)
from app.shared.pagination.dto import (
    PaginatedDTO,
)

class CouponService:

    def __init__(
        self,
        *,
        coupon_repository: CouponRepository,
        coupon_redemption_repository: CouponRedemptionRepository,
        coupon_resolver: CouponResolver,
        pagination_service: PaginationService,
    ) -> None:

        self._coupon_repository = coupon_repository

        self._coupon_redemption_repository = (
            coupon_redemption_repository
        )

        self._coupon_resolver = coupon_resolver

        self._pagination_service = pagination_service

    async def get_redemption_rows(
        self,
        *,
        coupon_id: int,
        page: int,
        limit: int,
    ) -> PaginatedDTO[CouponRedemption]:

        await self._coupon_repository.get_by_id(
            model_id=coupon_id,
        )

        offset = self._pagination_service.get_offset(
            page,
            limit,
        )

        items, total_items = (
            await self
            ._coupon_redemption_repository
            .get_rows_by_coupon(
                coupon_id=coupon_id,
                offset=offset,
                limit=limit,
            )
        )

        return PaginatedDTO.create(
            items=items,
            total_items=total_items,
            current_page=self._pagination_service.get_current_page(
                offset,
                limit,
            ),
            total_pages=self._pagination_service.get_total_pages(
                total_items,
                limit,
            ),
        )

    async def create(
        self,
        *,
        promotion_id: int,
        code: str,
        is_active: bool = True,
        starts_at: datetime | None = None,
        ends_at: datetime | None = None,
        max_redemptions: int | None = None,
        max_redemptions_per_customer: int | None = None,
    ) -> Coupon:

        coupon = Coupon(
            id=None,
            promotion_id=promotion_id,
            code=code.strip().upper(),
            is_active=is_active,
            starts_at=starts_at,
            ends_at=ends_at,
            max_redemptions=max_redemptions,
            max_redemptions_per_customer=max_redemptions_per_customer,
            used_count=0,
            created_at=None,
            updated_at=None,
        )

        coupon.validate()

        return await self._coupon_repository.save(
            entity=coupon,
        )

    async def get_by_id(
        self,
        *,
        coupon_id: int,
    ) -> Coupon:

        return await self._coupon_repository.get_by_id(
            model_id=coupon_id,
        )

    async def get_by_code(
        self,
        *,
        code: str,
    ) -> Coupon:

        coupon = await self._coupon_repository.get_by_code(
            code=code.strip().upper(),
        )

        if coupon is None:
            raise ValueNotFound(
                "El cupón no fue encontrado.",
                {
                    "service": "CouponService",
                    "event": "get_by_code",
                    "coupon_code": code,
                },
            )

        return coupon

    async def get_by_promotion(
        self,
        *,
        promotion_id: int,
    ) -> list[Coupon]:

        return await self._coupon_repository.get_by_promotion(
            promotion_id=promotion_id,
        )

    async def update(
        self,
        *,
        coupon_id: int,
        changes: dict,
    ) -> Coupon:

        coupon = await self._coupon_repository.get_by_id(
            model_id=coupon_id,
        )

        for field_name, value in changes.items():

            if field_name == "code" and value is not None:
                value = value.strip().upper()

            setattr(
                coupon,
                field_name,
                value,
            )

        coupon.updated_at = datetime.now(
            timezone.utc
        )

        coupon.validate()

        return await self._coupon_repository.save(
            entity=coupon,
        )

    async def toggle_status(
        self,
        *,
        coupon_id: int,
    ) -> None:

        coupon = await self._coupon_repository.get_by_id(
            model_id=coupon_id,
        )

        coupon.is_active = not coupon.is_active

        coupon.updated_at = datetime.now(
            timezone.utc
        )

        coupon.validate()

        await self._coupon_repository.save(
            entity=coupon,
        )

    async def delete(
        self,
        *,
        coupon_id: int,
    ) -> None:

        await self._coupon_repository.delete_by_id(
            model_id=coupon_id,
        )

    async def redeem(
        self,
        *,
        coupon_code: str,
        customer_id: int,
    ) -> CouponRedemption:

        coupon = await self._coupon_repository.get_by_code(
            code=coupon_code.strip().upper(),
            with_lock=True,
        )

        if coupon is None:
            raise ValueNotFound(
                "El cupón no fue encontrado.",
                {
                    "service": "CouponService",
                    "event": "redeem",
                    "coupon_code": coupon_code,
                    "customer_id": customer_id,
                },
            )

        now = datetime.now(timezone.utc)
        
        customer_redemptions = (
            await self._coupon_redemption_repository
            .count_by_coupon_and_customer(
                coupon_id=coupon.id,
                customer_id=customer_id,
            )
        )

        self._coupon_resolver.validate(
            coupon=coupon,
            customer_redemptions=customer_redemptions,
            now=now,
        )

        redemption = CouponRedemption(
            id=None,
            coupon_id=coupon.id,
            customer_id=customer_id,
            created_at=None,
        )

        redemption = (
            await self._coupon_redemption_repository.save(
                entity=redemption,
            )
        )

        coupon.used_count += 1
        coupon.updated_at = now

        await self._coupon_repository.save(
            entity=coupon,
        )

        return redemption