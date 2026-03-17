from pathlib import Path

from scanner import scan_folder
from normalizer import enrich_file_record
from exporters.csv_exporter import export_to_csv


def main() -> None:
    folder_input = input("Enter folder path to scan: ").strip()
    folder_path = Path(folder_input)

    try:
        files = scan_folder(folder_path)
    except (FileNotFoundError, NotADirectoryError) as error:
        print(f"Error: {error}")
        return

    print(f"\nFound {len(files)} supported file(s).\n")

    records = []

    for file_path in files:
        record = enrich_file_record(file_path)
        records.append(record)

    output_path = Path("output/metadata_index.csv")

    try:
        export_to_csv(records, output_path)
    except ValueError as error:
        print(f"Error: {error}")
        return

    print(f"CSV export complete: {output_path.resolve()}")


if __name__ == "__main__":
    main()
