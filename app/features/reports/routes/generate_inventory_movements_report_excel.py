from io import BytesIO
from typing import Annotated

from fastapi import Depends
from fastapi.responses import StreamingResponse

from app.features.reports.reports_route import router

from app.features.reports.dto import (
    GenerateInventoryMovementReportCommand
)

from app.features.reports.schema import (
    GenerateInventoryMovementReportSchema
)

from app.features.reports.use_cases.generate_inventory_movement_excel_report import (
    GenerateInventoryMovementExcelReportUseCase
)

from app.features.reports.use_cases.dependencies import (
    get_generate_inventory_movement_excel_report_use_case
)
from app.core.authorization.dependencies import require_any_permission
from app.core.authorization.permissions import Permission
from app.shared.datetime import to_datetime_range

from app.features.reports.constants import (
    REPORT_CONTEXT_NAMES
)
from app.features.reports.helpers import build_report_filename

@router.post(
    "/inventory-movements/excel",
    dependencies=[
        require_any_permission(
            Permission.REPORT_VIEW,
            Permission.REPORT_EXPORT
        )
    ]
)
async def generate_inventory_movement_excel_report(
    schema: GenerateInventoryMovementReportSchema,
    use_case: Annotated[
        GenerateInventoryMovementExcelReportUseCase,
        Depends(
            get_generate_inventory_movement_excel_report_use_case
        )
    ]
):
    data_range = to_datetime_range(schema.start_date, schema.end_date)
    filename = build_report_filename(
        context_name=REPORT_CONTEXT_NAMES[
            schema.owner_type
        ],
        start_date=data_range.start,
        end_date=data_range.end
    )
    command = (
        GenerateInventoryMovementReportCommand(
            owner_type=schema.owner_type,
            start_date=data_range.start,
            end_date=data_range.end
        )
    )

    excel_bytes = await use_case.execute(
        command
    )

    return StreamingResponse(
        BytesIO(excel_bytes),
        media_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
    )