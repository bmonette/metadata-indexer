from pathlib import Path

SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".mp3",
    ".pdf",
}


def is_supported_file(path: Path) -> bool:
    """
    Return True if the path is a file with a supported extension.
    Extension matching is case-insensitive.
    """
    return path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS


def scan_folder(folder_path: Path) -> list[Path]:
    """
    Recursively scan a folder and return a sorted list of supported files.

    Raises:
        FileNotFoundError: If the folder does not exist.
        NotADirectoryError: If the path is not a directory.
    """
    if not folder_path.exists():
        raise FileNotFoundError(f"Folder does not exist: {folder_path}")

    if not folder_path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {folder_path}")

    matching_files = [
        path for path in folder_path.rglob("*")
        if is_supported_file(path)
    ]

    return sorted(matching_files, key=lambda path: str(path).lower())
