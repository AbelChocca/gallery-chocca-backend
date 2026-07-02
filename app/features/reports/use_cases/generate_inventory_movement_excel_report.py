from app.features.reports.builders.inventory_movement_report_builder import InventoryMovementReportBuilder
from app.features.reports.generators.inventory_movement_report import InventoryMovementExcelReportGenerator
from app.features.reports.dto import GenerateInventoryMovementReportCommand

class GenerateInventoryMovementExcelReportUseCase:

    def __init__(
        self,
        builder:
            InventoryMovementReportBuilder,
        generator:
            InventoryMovementExcelReportGenerator
    ) -> None:

        self._builder = builder
        self._generator = generator

    async def execute(
        self,
        command: GenerateInventoryMovementReportCommand
    ) -> bytes:

        report_data = await self._builder.build(
            owner_type=command.owner_type,
            start_date=command.start_date,
            end_date=command.end_date
        )

        return self._generator.generate(
            report_data
        )