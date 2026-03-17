from pathlib import Path

from scanner import scan_folder
from file_info import build_file_record
from extractors.image_extractor import extract_image_metadata
from extractors.audio_extractor import extract_audio_metadata
from extractors.pdf_extractor import extract_pdf_metadata


def main() -> None:
    folder_input = input("Enter folder path to scan: ").strip()
    folder_path = Path(folder_input)

    try:
        files = scan_folder(folder_path)
    except (FileNotFoundError, NotADirectoryError) as error:
        print(f"Error: {error}")
        return

    print(f"\nFound {len(files)} supported file(s).\n")

    for file_path in files[:20]:
        record = build_file_record(file_path)

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

        print(record)
        print("-" * 60)


if __name__ == "__main__":
    main()
