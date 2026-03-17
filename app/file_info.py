from datetime import datetime
from pathlib import Path

from models import FileRecord


FILE_TYPE_MAP = {
    ".jpg": "image",
    ".jpeg": "image",
    ".png": "image",
    ".mp3": "audio",
    ".pdf": "pdf",
}


def format_timestamp(timestamp: float) -> str:
    """
    Convert a Unix timestamp into a readable local datetime string.
    """
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def get_file_type(extension: str) -> str:
    """
    Return a normalized file type based on the file extension.
    """
    return FILE_TYPE_MAP.get(extension.lower(), "unknown")


def build_file_record(file_path: Path) -> FileRecord:
    """
    Build a FileRecord with generic file metadata only.
    Type-specific metadata is left as None for now.
    """
    stat = file_path.stat()

    return FileRecord(
        file_name=file_path.name,
        extension=file_path.suffix.lower(),
        file_type=get_file_type(file_path.suffix),
        full_path=str(file_path.resolve()),
        parent_folder=file_path.parent.name,
        size_bytes=stat.st_size,
        size_kb=round(stat.st_size / 1024, 2),
        created_time=format_timestamp(stat.st_ctime),
        modified_time=format_timestamp(stat.st_mtime),
        scan_status="success",
        error_message=None,
    )
