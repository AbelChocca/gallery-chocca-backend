from datetime import datetime


def build_report_filename(
    *,
    context_name: str,
    start_date: datetime,
    end_date: datetime
) -> str:

    safe_context = (
        context_name.upper()
        .replace(" ", "_")
    )

    return (
        f"REPORTE_MOVIMIENTOS_"
        f"{safe_context}_"
        f"DESDE_{start_date:%d-%m-%Y}_HASTA_"
        f"{end_date:%d-%m-%Y}.xlsx"
    )