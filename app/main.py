from pathlib import Path

from scanner import scan_folder
from normalizer import enrich_file_record
from exporters.csv_exporter import export_to_csv
from exporters.excel_exporter import export_to_excel
from reporting import generate_summary


def main() -> None:
    folder_input = input("Enter folder path to scan: ").strip()
    folder_path = Path(folder_input)

    try:
        files = scan_folder(folder_path)
    except (FileNotFoundError, NotADirectoryError) as error:
        print(f"Error: {error}")
        return

    print(f"\nFound {len(files)} supported file(s).\n")

    print("Processing files...")

    records = []

    for file_path in files:
        record = enrich_file_record(file_path)
        records.append(record)

    if not records:
        print("No supported files found. Nothing to export.")
        return

    csv_output = Path("output/metadata_index.csv")
    excel_output = Path("output/metadata_index.xlsx")

    try:
        export_to_csv(records, csv_output)
        export_to_excel(records, excel_output)
    except ValueError as error:
        print(f"Error: {error}")
        return

    print(f"\nCSV export complete: {csv_output.resolve()}")
    print(f"Excel export complete: {excel_output.resolve()}")

    summary = generate_summary(records)

    print("\nSummary:")
    print(f"Total files: {summary['total_files']}")
    print(f"Success: {summary['success_count']}")
    print(f"Errors: {summary['error_count']}")
    print(f"Total size (KB): {summary['total_size_kb']}")

    print("\nBy file type:")
    for file_type, count in summary["file_types"].items():
        print(f"  {file_type}: {count}")


if __name__ == "__main__":
    main()
