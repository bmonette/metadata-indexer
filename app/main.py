from pathlib import Path

from scanner import scan_folder
from normalizer import enrich_file_record


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
        record = enrich_file_record(file_path)
        print(record)
        print("-" * 60)


if __name__ == "__main__":
    main()
