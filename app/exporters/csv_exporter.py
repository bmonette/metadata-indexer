import csv
from dataclasses import asdict
from pathlib import Path

from models import FileRecord


def export_to_csv(records: list[FileRecord], output_path: Path) -> None:
    """
    Export a list of FileRecord objects to a CSV file.
    """
    if not records:
        raise ValueError("No records to export.")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(asdict(records[0]).keys())

    with output_path.open("w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for record in records:
            writer.writerow(asdict(record))