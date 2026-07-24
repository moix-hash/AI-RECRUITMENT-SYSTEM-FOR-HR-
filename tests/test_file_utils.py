from __future__ import annotations

from utils.file_utils import clean_extracted_text


def test_clean_extracted_text_normalizes_pdf_whitespace() -> None:
    assert clean_extracted_text("  Python\t\tSQL\r\n\r\n\r\nAWS\x00 ") == "Python SQL\n\nAWS"
