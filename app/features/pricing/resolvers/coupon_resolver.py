from datetime import datetime

from app.features.pricing.entities.coupon import Coupon
from app.core.exceptions import ValidationError


class CouponResolver:
    def validate(
        self,
        *,
        coupon: Coupon,
        now: datetime,
    ) -> None:
        self._validate_active(coupon=coupon)
        self._validate_start_date(
            coupon=coupon,
            now=now,
        )
        self._validate_end_date(
            coupon=coupon,
            now=now,
        )
        self._validate_redemptions(coupon=coupon)

    def _validate_active(
        self,
        *,
        coupon: Coupon,
    ) -> None:
        if not coupon.is_active:
            raise ValidationError("El cupon esta inactivo.")

    def _validate_start_date(
        self,
        *,
        coupon: Coupon,
        now: datetime,
    ) -> None:
        if (
            coupon.starts_at is not None
            and now < coupon.starts_at
        ):
            raise ValidationError("El cupon ya no esta disponible.")

    def _validate_end_date(
        self,
        *,
        coupon: Coupon,
        now: datetime,
    ) -> None:
        if (
            coupon.ends_at is not None
            and now >= coupon.ends_at
        ):
            raise ValidationError("El cupon ha expirado.")

    def _validate_redemptions(
        self,
        *,
        coupon: Coupon,
    ) -> None:
        if (
            coupon.max_redemptions is not None
            and coupon.used_count >= coupon.max_redemptions
        ):
            raise ValidationError("El cupon alcanzo el maximo numero de canjeos.")