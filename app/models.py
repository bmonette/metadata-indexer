from dataclasses import dataclass
from typing import Optional


@dataclass
class FileRecord:
    # ===== Generic file info =====
    file_name: str
    extension: str
    file_type: str
    full_path: str
    parent_folder: str

    size_bytes: int
    size_kb: float

    created_time: str
    modified_time: str

    scan_status: str
    error_message: Optional[str] = None

    # ===== Image metadata =====
    image_width: Optional[int] = None
    image_height: Optional[int] = None
    image_format: Optional[str] = None
    exif_make: Optional[str] = None
    exif_model: Optional[str] = None
    exif_datetime: Optional[str] = None

    # ===== Audio metadata =====
    audio_title: Optional[str] = None
    audio_artist: Optional[str] = None
    audio_album: Optional[str] = None
    audio_duration_seconds: Optional[float] = None
    audio_bitrate: Optional[int] = None
    audio_sample_rate: Optional[int] = None

    # ===== PDF metadata =====
    pdf_title: Optional[str] = None
    pdf_author: Optional[str] = None
    pdf_subject: Optional[str] = None
    pdf_pages: Optional[int] = None
    pdf_text_snippet: Optional[str] = None
