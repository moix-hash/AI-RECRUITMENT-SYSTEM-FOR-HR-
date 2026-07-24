from __future__ import annotations

import re
from typing import List


class PromptGuard:
    """Sanitize candidate text before AI processing to reduce prompt injection risk."""

    def sanitize(self, text: str) -> str:
        cleaned = text or ""
        cleaned = cleaned.replace("\x00", "")
        cleaned = re.sub(r"(?i)(ignore previous instructions|system prompt|jailbreak|override instructions)", "", cleaned)
        cleaned = re.sub(r"<[^>]+>", "", cleaned)
        return cleaned.strip()

    def extract_sensitive(self, text: str) -> List[str]:
        return re.findall(r"(?i)(api[_ -]?key|token|secret)", text)
