from collections import Counter
from dataclasses import asdict

from models import FileRecord


def generate_summary(records: list[FileRecord]) -> dict:
    """
    Generate summary statistics from FileRecord objects.
    """
    total_files = len(records)

    success_count = sum(1 for r in records if r.scan_status == "success")
    error_count = sum(1 for r in records if r.scan_status == "error")

    file_types = Counter(r.file_type for r in records)

    total_size_bytes = sum(r.size_bytes for r in records)
    total_size_kb = round(total_size_bytes / 1024, 2)

    return {
        "total_files": total_files,
        "success_count": success_count,
        "error_count": error_count,
        "file_types": dict(file_types),
        "total_size_bytes": total_size_bytes,
        "total_size_kb": total_size_kb,
    }
