from pathlib import Path
from typing import Optional

from PIL import Image, ExifTags


EXIF_TAGS = {value: key for key, value in ExifTags.TAGS.items()}


def get_exif_value(exif_data: dict, tag_name: str) -> Optional[str]:
    """
    Return a specific EXIF value by tag name if it exists.
    """
    tag_id = EXIF_TAGS.get(tag_name)
    if tag_id is None:
        return None

    value = exif_data.get(tag_id)
    if value is None:
        return None

    return str(value)


def extract_image_metadata(file_path: Path) -> dict:
    """
    Extract image metadata from a supported image file.
    Returns a dictionary of image-related fields only.
    """
    with Image.open(file_path) as image:
        metadata = {
            "image_width": image.width,
            "image_height": image.height,
            "image_format": image.format,
            "exif_make": None,
            "exif_model": None,
            "exif_datetime": None,
        }

        exif_data = image.getexif()

        if exif_data:
            metadata["exif_make"] = get_exif_value(exif_data, "Make")
            metadata["exif_model"] = get_exif_value(exif_data, "Model")
            metadata["exif_datetime"] = get_exif_value(exif_data, "DateTime")

        return metadata