from __future__ import annotations

import os
import re
import shutil
from pathlib import Path
from typing import List, Tuple

import fitz
import pdfplumber

from config.settings import MAX_UPLOAD_SIZE_MB


UPLOAD_DIR = Path(__file__).resolve().parents[1] / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def clean_extracted_text(text: str) -> str:
    """Normalize PDF extraction output without changing meaningful resume content."""
    normalized = (text or "").replace("\x00", "").replace("\r", "\n")
    normalized = re.sub(r"[ \t]+", " ", normalized)
    normalized = re.sub(r"\n{3,}", "\n\n", normalized)
    return normalized.strip()


def validate_file_size(file_obj, max_size_mb: int = MAX_UPLOAD_SIZE_MB) -> bool:
    file_obj.seek(0, os.SEEK_END)
    size = file_obj.tell()
    file_obj.seek(0)
    return size <= max_size_mb * 1024 * 1024


def extract_text_from_pdf(file_path: str) -> str:
    text_chunks: List[str] = []
    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                text_chunks.append(page.get_text())
    except Exception:
        text_chunks = []

    if "".join(text_chunks).strip():
        return clean_extracted_text("\n".join(text_chunks))

    try:
        with pdfplumber.open(file_path) as doc:
            for page in doc.pages:
                text_chunks.append(page.extract_text() or "")
    except Exception:
        return ""
    return clean_extracted_text("\n".join(text_chunks))


def save_upload(file_obj, filename: str) -> Tuple[str, str]:
    safe_name = Path(filename).name.replace(" ", "_")
    storage_path = UPLOAD_DIR / safe_name
    with storage_path.open("wb") as buffer:
        shutil.copyfileobj(file_obj, buffer)
    return str(storage_path), safe_name
