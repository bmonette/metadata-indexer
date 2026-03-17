from dataclasses import asdict
from pathlib import Path

from openpyxl import Workbook
from openpyxl.utils import get_column_letter

from models import FileRecord


def auto_adjust_column_width(worksheet) -> None:
    """
    Adjust column widths based on max content length.
    """
    for column_cells in worksheet.columns:
        max_length = 0
        column_letter = get_column_letter(column_cells[0].column)

        for cell in column_cells:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))

        adjusted_width = min(max_length + 2, 60)  # cap width
        worksheet.column_dimensions[column_letter].width = adjusted_width


def export_to_excel(records: list[FileRecord], output_path: Path) -> None:
    """
    Export FileRecord objects to an Excel file.
    """
    if not records:
        raise ValueError("No records to export.")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Metadata Index"

    # Headers
    headers = list(asdict(records[0]).keys())
    sheet.append(headers)

    # Data rows
    for record in records:
        row = list(asdict(record).values())
        sheet.append(row)

    # Freeze header row
    sheet.freeze_panes = "A2"

    # Auto-size columns
    auto_adjust_column_width(sheet)

    workbook.save(output_path)
