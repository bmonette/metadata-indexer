from pathlib import Path

from file_info import build_file_record
from extractors.image_extractor import extract_image_metadata
from extractors.audio_extractor import extract_audio_metadata
from extractors.pdf_extractor import extract_pdf_metadata
from models import FileRecord


def enrich_file_record(file_path: Path) -> FileRecord:
    """
    Build a FileRecord with generic metadata and enrich it with
    type-specific metadata when supported.
    """
    record = build_file_record(file_path)

    try:
        if record.file_type == "image":
            image_data = extract_image_metadata(file_path)
            record.image_width = image_data["image_width"]
            record.image_height = image_data["image_height"]
            record.image_format = image_data["image_format"]
            record.exif_make = image_data["exif_make"]
            record.exif_model = image_data["exif_model"]
            record.exif_datetime = image_data["exif_datetime"]

        elif record.file_type == "audio":
            audio_data = extract_audio_metadata(file_path)
            record.audio_title = audio_data["audio_title"]
            record.audio_artist = audio_data["audio_artist"]
            record.audio_album = audio_data["audio_album"]
            record.audio_duration_seconds = audio_data["audio_duration_seconds"]
            record.audio_bitrate = audio_data["audio_bitrate"]
            record.audio_sample_rate = audio_data["audio_sample_rate"]

        elif record.file_type == "pdf":
            pdf_data = extract_pdf_metadata(file_path)
            record.pdf_title = pdf_data["pdf_title"]
            record.pdf_author = pdf_data["pdf_author"]
            record.pdf_subject = pdf_data["pdf_subject"]
            record.pdf_pages = pdf_data["pdf_pages"]
            record.pdf_text_snippet = pdf_data["pdf_text_snippet"]

    except Exception as e:
        record.scan_status = "error"
        record.error_message = str(e)

    return record
