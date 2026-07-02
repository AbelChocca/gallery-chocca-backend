from datetime import date, datetime, time
from zoneinfo import ZoneInfo
from dataclasses import dataclass

LIMA_TZ = ZoneInfo("America/Lima")
UTC = ZoneInfo("UTC")

@dataclass(frozen=True)
class DateRange:
    start: datetime | None
    end: datetime | None


def to_datetime_range(
    start: date | None = None,
    end: date | None = None,
) -> DateRange:

    start_dt = None
    end_dt = None

    if start is not None:
        start_dt = datetime.combine(
            start,
            time.min,
            tzinfo=LIMA_TZ,
        ).astimezone(UTC)

    if end is not None:
        end_dt = datetime.combine(
            end,
            time.max,
            tzinfo=LIMA_TZ,
        ).astimezone(UTC)

    return DateRange(
        start=start_dt,
        end=end_dt,
    )