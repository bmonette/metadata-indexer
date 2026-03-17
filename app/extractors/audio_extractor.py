from pathlib import Path
from typing import Optional

from mutagen import File
from mutagen.easyid3 import EasyID3


def get_first_tag_value(tags: EasyID3, key: str) -> Optional[str]:
    """
    Return the first value for an ID3 tag if it exists.
    """
    if tags is None:
        return None

    value = tags.get(key)
    if not value:
        return None

    return str(value[0])


def extract_audio_metadata(file_path: Path) -> dict:
    """
    Extract MP3 metadata and audio properties.
    Returns a dictionary of audio-related fields only.
    """
    metadata = {
        "audio_title": None,
        "audio_artist": None,
        "audio_album": None,
        "audio_duration_seconds": None,
        "audio_bitrate": None,
        "audio_sample_rate": None,
    }

    audio = File(file_path, easy=True)
    if audio is None:
        return metadata

    metadata["audio_title"] = get_first_tag_value(audio, "title")
    metadata["audio_artist"] = get_first_tag_value(audio, "artist")
    metadata["audio_album"] = get_first_tag_value(audio, "album")

    full_audio = File(file_path)
    if full_audio is not None and hasattr(full_audio, "info"):
        info = full_audio.info

        if hasattr(info, "length"):
            metadata["audio_duration_seconds"] = round(info.length, 2)

        if hasattr(info, "bitrate") and info.bitrate is not None:
            metadata["audio_bitrate"] = int(info.bitrate)

        if hasattr(info, "sample_rate") and info.sample_rate is not None:
            metadata["audio_sample_rate"] = int(info.sample_rate)

    return metadata
