from datetime import date, datetime, timedelta
from collections.abc import Collection

from app.core.exceptions import ValidationError

from app.shared.calendar.holidays.peru_2026 import PERU_HOLIDAYS_2026


class BusinessDayService:
    MAX_BUSINESS_DAYS = 365

    def __init__(
        self,
        holidays: Collection[date] | None = None,
    ):
        self._holidays = frozenset(holidays or [])

    def add_business_days(
        self,
        *,
        current: date | datetime,
        days: int,
    ) -> date | datetime:
        if type(days) is not int:
            raise ValidationError(
                "La cantidad de días debe ser un entero."
            )

        if not 1 <= days <= self.MAX_BUSINESS_DAYS:
            raise ValidationError(
                "Los días hábiles deben estar entre 1 y 365."
            )

        result = current
        remaining = days

        
        while remaining > 0:
            result += timedelta(days=1)

            current_date = (
                result.date()
                if isinstance(result, datetime)
                else result
            )

            if current_date.weekday() >= 6:
                continue

            if current_date in self._holidays:
                continue

            remaining -= 1

        return result


def get_business_day_service() -> BusinessDayService:
    return BusinessDayService(
        holidays=PERU_HOLIDAYS_2026,
    )