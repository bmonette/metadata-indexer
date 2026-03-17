from pathlib import Path

from scanner import scan_folder
from file_info import build_file_record
from extractors.image_extractor import extract_image_metadata


def main() -> None:
    folder_input = input("Enter folder path to scan: ").strip()
    folder_path = Path(folder_input)

    try:
        files = scan_folder(folder_path)
    except (FileNotFoundError, NotADirectoryError) as error:
        print(f"Error: {error}")
        return

    print(f"\nFound {len(files)} supported file(s).\n")

    for file_path in files[:10]:
        record = build_file_record(file_path)

        if record.file_type == "image":
            image_data = extract_image_metadata(file_path)

            record.image_width = image_data["image_width"]
            record.image_height = image_data["image_height"]
            record.image_format = image_data["image_format"]
            record.exif_make = image_data["exif_make"]
            record.exif_model = image_data["exif_model"]
            record.exif_datetime = image_data["exif_datetime"]

        print(record)
        print("-" * 60)


if __name__ == "__main__":
    main()
