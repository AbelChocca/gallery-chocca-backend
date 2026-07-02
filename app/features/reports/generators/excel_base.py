from abc import ABC, abstractmethod
from io import BytesIO
from datetime import datetime

import xlsxwriter
from xlsxwriter import Workbook
from xlsxwriter.worksheet import Worksheet
from xlsxwriter.format import Format

from app.features.reports.dto import ColumnDefinition
from app.features.reports.constants import LIMA_TZ

class BaseExcelReportGenerator(ABC):

    TITLE_ROW = 0
    PERIOD_ROW = 2
    GENERATED_ROW = 3
    HEADER_ROW = 5
    DATA_START_ROW = 6

    def _create_workbook(
        self
    ) -> tuple[Workbook, BytesIO]:

        buffer = BytesIO()

        workbook = xlsxwriter.Workbook(
            buffer,
            {
                "in_memory": True
            }
        )

        return workbook, buffer

    def _workbook_to_bytes(
        self,
        workbook: Workbook,
        buffer: BytesIO
    ) -> bytes:

        workbook.close()
        buffer.seek(0)

        return buffer.getvalue()
    
    def format_lima_datetime(self, dt: datetime) -> str:
        return dt.astimezone(LIMA_TZ).strftime("%d/%m/%Y %H:%M")
    
    def format_lima_date(
        self,
        dt: datetime
    ) -> str:
        return (
            dt.astimezone(LIMA_TZ)
            .strftime("%d/%m/%Y")
        )
    
    def _to_excel_datetime(self, value: datetime):
        if value.tzinfo is None:
            return value

        return value.astimezone(LIMA_TZ).replace(tzinfo=None)
    
    def _write_title(
        self,
        worksheet: Worksheet,
        title: str,
        total_columns: int,
        title_format: Format
    ) -> None:

        worksheet.merge_range(
            self.TITLE_ROW,
            0,
            self.TITLE_ROW,
            total_columns - 1,
            title,
            title_format
        )

    def _write_metadata(
        self,
        worksheet: Worksheet,
        period: str,
        generated_at: str,
        metadata_format: Format
    ) -> None:

        worksheet.write(
            self.PERIOD_ROW,
            0,
            f"Periodo: {period}",
            metadata_format
        )

        worksheet.write(
            self.GENERATED_ROW,
            0,
            f"Generado: {generated_at}",
            metadata_format
        )
    
    def _write_headers(
        self,
        worksheet: Worksheet,
        columns: list[ColumnDefinition],
        header_format
    ) -> None:
        for column_index, column in enumerate(columns):
            worksheet.write(
                self.HEADER_ROW,
                column_index,
                column.header,
                header_format
            )

    def _set_columns_width(
        self,
        worksheet: Worksheet,
        columns: list[ColumnDefinition]
    ) -> None:

        for column_index, column in enumerate(columns):
            worksheet.set_column(
                column_index,
                column_index,
                column.width
            )

    def _apply_autofilter(
        self,
        worksheet: Worksheet,
        data_count: int,
        last_col: int
    ) -> None:
        last_row = self.HEADER_ROW + data_count

        worksheet.autofilter(
            self.HEADER_ROW,
            0,
            last_row,
            last_col
        )

    def _freeze_header(
        self,
        worksheet: Worksheet,
    ) -> None:

        worksheet.freeze_panes(
            self.HEADER_ROW + 1,
            0
        )

    def _get_last_column(
        self,
        columns: list[ColumnDefinition]
    ) -> int:

        return len(columns) - 1
    
    def _get_last_data_row(
        self,
        data_count: int
    ) -> int:

        return self.HEADER_ROW + data_count
    
    def _create_title_format(
        self,
        workbook: Workbook
    ) -> Format:
        return workbook.add_format(
            {
                "bold": True,
                "font_size": 16
            }
        )
    
    def _create_date_format(
        self,
        workbook: Workbook
    ) -> Format:

        return workbook.add_format(
            {
                "num_format": "dd/mm/yyyy hh:mm"
            }
        )
    
    def _create_integer_format(
        self,
        workbook: Workbook
    ) -> Format:

        return workbook.add_format(
            {
                "num_format": "#,##0"
            }
        )

    def _create_header_format(
        self,
        workbook: Workbook
    ) -> Format:
        return workbook.add_format(
            {
                "bold": True,
                "border": 1,
                "align": "center"
            }
        )
    
    def _create_metadata_format(
        self,
        workbook: Workbook
    ) -> Format:

        return workbook.add_format(
            {
                "italic": True
            }
        )

    @abstractmethod
    def generate(self, report_data) -> bytes:
        ...