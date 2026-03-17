from pathlib import Path

from pypdf import PdfReader


def clean_pdf_value(value) -> str | None:
    """
    Convert a PDF metadata value to a clean string.
    """
    if value is None:
        return None

    value = str(value).strip()
    return value if value else None


def extract_pdf_text_snippet(reader: PdfReader, max_chars: int = 300) -> str | None:
    """
    Extract a short text snippet from the first pages of a PDF.
    """
    collected_text = []

    for page in reader.pages[:3]:
        text = page.extract_text()
        if text:
            cleaned = " ".join(text.split())
            if cleaned:
                collected_text.append(cleaned)

        combined = " ".join(collected_text).strip()
        if len(combined) >= max_chars:
            return combined[:max_chars]

    combined = " ".join(collected_text).strip()
    return combined[:max_chars] if combined else None


def extract_pdf_metadata(file_path: Path) -> dict:
    """
    Extract PDF metadata, page count, and a short text snippet.
    Returns a dictionary of PDF-related fields only.
    """
    metadata = {
        "pdf_title": None,
        "pdf_author": None,
        "pdf_subject": None,
        "pdf_pages": None,
        "pdf_text_snippet": None,
    }

    reader = PdfReader(str(file_path))
    doc_info = reader.metadata

    metadata["pdf_pages"] = len(reader.pages)

    if doc_info:
        metadata["pdf_title"] = clean_pdf_value(doc_info.get("/Title"))
        metadata["pdf_author"] = clean_pdf_value(doc_info.get("/Author"))
        metadata["pdf_subject"] = clean_pdf_value(doc_info.get("/Subject"))

    metadata["pdf_text_snippet"] = extract_pdf_text_snippet(reader)

    return metadata
