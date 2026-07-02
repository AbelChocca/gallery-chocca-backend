from app.features.reports.dto import InventoryMovementReportData, InventoryOwnerSummaryRow, InventoryMovementReportRow, InventoryReportMetrics
from app.features.reports.generators.excel_base import BaseExcelReportGenerator
from app.features.reports.constants import METRICS_COLUMNS, SUMMARY_COLUMNS, MOVEMENTS_COLUMNS

from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet

class InventoryMovementExcelReportGenerator(BaseExcelReportGenerator):

    def generate(
        self,
        report_data: InventoryMovementReportData
    ) -> bytes:

        workbook, buffer = self._create_workbook()

        self._build_movements_sheet(
            workbook,
            report_data
        )

        self._build_summary_sheet(
            workbook,
            report_data
        )

        self._build_metrics_sheet(
            workbook,
            report_data
        )

        return self._workbook_to_bytes(
            workbook,
            buffer
        )

    def _build_movements_sheet(
        self,
        workbook: Workbook,
        report_data: InventoryMovementReportData
    ) -> None:

        worksheet = workbook.add_worksheet(
            "Movimientos"
        )

        title_format = self._create_title_format(
            workbook
        )

        metadata_format = self._create_metadata_format(
            workbook
        )

        header_format = self._create_header_format(
            workbook
        )

        date_format = self._create_date_format(
            workbook
        )

        integer_format = self._create_integer_format(
            workbook
        )

        self._write_title(
            worksheet,
            (
                f"REPORTE DE MOVIMIENTOS "
                f"DE {report_data.metadata.title.upper()}"
            ),
            len(MOVEMENTS_COLUMNS),
            title_format
        )

        self._write_metadata(
            worksheet,
            period=(
                f"{self.format_lima_date(report_data.metadata.start_date)}"
                f" - "
                f"{self.format_lima_date(report_data.metadata.end_date)}"
            ),
            generated_at=(
                self.format_lima_datetime(report_data.metadata.generated_at)
            ),
            metadata_format=metadata_format
        )

        self._set_columns_width(
            worksheet,
            MOVEMENTS_COLUMNS
        )

        self._write_headers(
            worksheet,
            MOVEMENTS_COLUMNS,
            header_format
        )

        self._freeze_header(
            worksheet
        )

        self._write_movement_rows(
            worksheet,
            report_data.movements,
            date_format,
            integer_format
        )

        self._apply_autofilter(
            worksheet,
            data_count=len(report_data.movements),
            last_col=self._get_last_column(
                MOVEMENTS_COLUMNS
            )
        )

    def _write_movement_rows(
        self,
        worksheet: Worksheet,
        movements: list[InventoryMovementReportRow],
        date_format,
        integer_format
    ) -> None:

        row = self.DATA_START_ROW

        for movement in movements:

            worksheet.write_datetime(
                row,
                0,
                self._to_excel_datetime(movement.movement_date),
                date_format
            )

            worksheet.write(
                row,
                1,
                movement.owner_code
            )

            worksheet.write(
                row,
                2,
                movement.owner_name
            )

            worksheet.write(
                row,
                3,
                movement.movement_type.value
            )

            worksheet.write(
                row,
                4,
                movement.movement_reason
            )

            worksheet.write_number(
                row,
                5,
                movement.previous_stock,
                integer_format
            )

            worksheet.write_number(
                row,
                6,
                movement.quantity,
                integer_format
            )

            worksheet.write_number(
                row,
                7,
                movement.new_stock,
                integer_format
            )

            row += 1

    def _build_summary_sheet(
        self,
        workbook: Workbook,
        report_data: InventoryMovementReportData
    ) -> None:

        worksheet = workbook.add_worksheet(
            "Resumen"
        )

        title_format = self._create_title_format(
            workbook
        )

        metadata_format = self._create_metadata_format(
            workbook
        )

        header_format = self._create_header_format(
            workbook
        )

        integer_format = self._create_integer_format(
            workbook
        )

        self._write_title(
            worksheet,
            (
                f"RESUMEN DE "
                f"{report_data.metadata.title.upper()}"
            ),
            len(SUMMARY_COLUMNS),
            title_format
        )

        self._write_metadata(
            worksheet,
            period=(
                f"{self.format_lima_date(report_data.metadata.start_date)}"
                f" - "
                f"{self.format_lima_date(report_data.metadata.end_date)}"
            ),
            generated_at=(
                self.format_lima_datetime(report_data.metadata.generated_at)
            ),
            metadata_format=metadata_format
        )

        self._set_columns_width(
            worksheet,
            SUMMARY_COLUMNS
        )

        self._write_headers(
            worksheet,
            SUMMARY_COLUMNS,
            header_format
        )

        self._freeze_header(
            worksheet
        )

        self._write_summary_rows(
            worksheet,
            report_data.material_summaries,
            integer_format
        )

        self._apply_autofilter(
            worksheet,
            data_count=len(
                report_data.material_summaries
            ),
            last_col=self._get_last_column(
                SUMMARY_COLUMNS
            )
        )

    def _write_summary_rows(
        self,
        worksheet: Worksheet,
        summaries: list[InventoryOwnerSummaryRow],
        integer_format
    ) -> None:

        row = self.DATA_START_ROW

        for summary in summaries:

            worksheet.write(
                row,
                0,
                summary.owner_name
            )

            worksheet.write_number(
                row,
                1,
                summary.total_entries,
                integer_format
            )

            worksheet.write_number(
                row,
                2,
                summary.total_sales,
                integer_format
            )

            worksheet.write_number(
                row,
                3,
                summary.total_customer_returns,
                integer_format
            )

            worksheet.write_number(
                row,
                4,
                summary.total_supplier_returns,
                integer_format
            )

            worksheet.write_number(
                row,
                5,
                summary.manual_adjustment_increase,
                integer_format
            )

            worksheet.write_number(
                row,
                6,
                summary.manual_adjustment_decrease,
                integer_format
            )

            worksheet.write_number(
                row,
                7,
                summary.final_stock,
                integer_format
            )

            row += 1

    def _build_metrics_sheet(
        self,
        workbook: Workbook,
        report_data: InventoryMovementReportData
    ) -> None:

        worksheet = workbook.add_worksheet(
            "KPIs"
        )

        title_format = self._create_title_format(
            workbook
        )

        metadata_format = self._create_metadata_format(
            workbook
        )

        header_format = self._create_header_format(
            workbook
        )

        integer_format = self._create_integer_format(
            workbook
        )

        self._write_title(
            worksheet,
            (
                f"KPIs DE "
                f"{report_data.metadata.title.upper()}"
            ),
            len(METRICS_COLUMNS),
            title_format
        )

        self._write_metadata(
            worksheet,
            period=(
                f"{self.format_lima_date(report_data.metadata.start_date)}"
                f" - "
                f"{self.format_lima_date(report_data.metadata.end_date)}"
            ),
            generated_at=(
                self.format_lima_datetime(report_data.metadata.generated_at)
            ),
            metadata_format=metadata_format
        )

        self._set_columns_width(
            worksheet,
            METRICS_COLUMNS
        )

        self._write_headers(
            worksheet,
            METRICS_COLUMNS,
            header_format
        )

        self._freeze_header(
            worksheet
        )

        self._write_metrics_rows(
            worksheet,
            report_data.metrics,
            integer_format
        )

        self._apply_autofilter(
            worksheet,
            data_count=8,
            last_col=self._get_last_column(
                METRICS_COLUMNS
            )
        )

    def _write_metrics_rows(
        self,
        worksheet: Worksheet,
        metrics: InventoryReportMetrics,
        integer_format
    ) -> None:

        rows = [
            (
                "Movimientos Totales",
                metrics.total_movements
            ),
            (
                "Entradas Totales",
                metrics.total_entries
            ),
            (
                "Ventas Totales",
                metrics.total_sales
            ),
            (
                "Devoluciones de Clientes",
                metrics.total_customer_returns
            ),
            (
                "Devoluciones a Proveedores",
                metrics.total_supplier_returns
            ),
            (
                "Ajustes Positivos",
                metrics.total_manual_adjustment_increase
            ),
            (
                "Ajustes Negativos",
                metrics.total_manual_adjustment_decrease
            ),
            (
                "Items Afectados",
                metrics.affected_owners
            )
        ]

        row = self.DATA_START_ROW

        for metric_name, value in rows:

            worksheet.write(
                row,
                0,
                metric_name
            )

            worksheet.write_number(
                row,
                1,
                value,
                integer_format
            )

            row += 1