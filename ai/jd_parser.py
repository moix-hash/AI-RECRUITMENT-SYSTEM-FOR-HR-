from __future__ import annotations

from typing import List

from ai.schemas import ParsedJobDescription
from ai.validators import sanitize_resume_text


def parse_job_description(description: str) -> ParsedJobDescription:
    cleaned = sanitize_resume_text(description)
    joined = " ".join(line.strip() for line in cleaned.splitlines() if line.strip())

    return ParsedJobDescription(
        job_title=_find_best_match(joined, ["title", "job title"]),
        department=_find_best_match(joined, ["department", "team"]),
        experience_required=_find_best_match(joined, ["experience", "years"]),
        required_skills=_extract_keywords(joined, ["required skills", "skills"]),
        preferred_skills=_extract_keywords(joined, ["preferred skills", "nice to have"]),
        education=_find_best_match(joined, ["education", "degree"]),
        responsibilities=_find_best_match(joined, ["responsibilities", "responsibilities include"]),
        tools=_extract_keywords(joined, ["tools", "tool"]),
        frameworks=_extract_keywords(joined, ["frameworks", "framework"]),
        soft_skills=_extract_keywords(joined, ["soft skills", "communication", "collaboration"]),
        certifications=_extract_keywords(joined, ["certifications", "certification"]),
        keywords=_extract_keywords(joined, ["skill", "experience", "certification", "management"]),
    )


def _find_best_match(text: str, patterns: List[str]) -> str:
    lower = text.lower()
    for pattern in patterns:
        if pattern in lower:
            start = lower.find(pattern)
            excerpt = text[start : start + 220]
            return excerpt.strip() or "Not Found"
    return "Not Found"


def _extract_keywords(text: str, patterns: List[str]) -> List[str]:
    lower = text.lower()
    results: List[str] = []
    for pattern in patterns:
        if pattern in lower:
            start = lower.find(pattern)
            excerpt = text[start : start + 250]
            values = [item.strip() for item in excerpt.split(",") if item.strip()]
            results.extend(values)
    seen = set()
    ordered: List[str] = []
    for value in results:
        normalized = value.strip()
        if normalized and normalized.lower() not in seen:
            ordered.append(normalized)
            seen.add(normalized.lower())
    return ordered
