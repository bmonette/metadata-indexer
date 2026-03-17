import csv
from dataclasses import asdict
from pathlib import Path

from models import FileRecord


ALWAYS_INCLUDE_COLUMNS = [
    "file_name",
    "extension",
    "file_type",
    "full_path",
    "parent_folder",
    "size_bytes",
    "size_kb",
    "created_time",
    "modified_time",
    "scan_status",
    "error_message",
]


def get_used_columns(record_dicts: list[dict]) -> list[str]:
    """
    Return a list of columns to export.
    Core columns are always included.
    Metadata columns are only included if at least one record
    contains a non-empty value for that column.
    """
    if not record_dicts:
        return ALWAYS_INCLUDE_COLUMNS.copy()

    all_columns = list(record_dicts[0].keys())
    used_columns = []

    for column in all_columns:
        if column in ALWAYS_INCLUDE_COLUMNS:
            used_columns.append(column)
            continue

        has_value = any(
            record.get(column) not in (None, "", [])
            for record in record_dicts
        )

        if has_value:
            used_columns.append(column)

    return used_columns


def export_to_csv(records: list[FileRecord], output_path: Path) -> None:
    """
    Export a list of FileRecord objects to a CSV file.
    """
    if not records:
        raise ValueError("No records to export.")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    record_dicts = [asdict(record) for record in records]
    fieldnames = get_used_columns(record_dicts)

    with output_path.open("w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for record_dict in record_dicts:
            filtered_row = {column: record_dict.get(column) for column in fieldnames}
            writer.writerow(filtered_row)
