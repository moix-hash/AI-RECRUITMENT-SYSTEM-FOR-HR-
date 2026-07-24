from __future__ import annotations

import re

from ai.schemas import ParsedResume
from ai.validators import normalize_not_found, sanitize_resume_text


def parse_resume_text(resume_text: str) -> ParsedResume:
    cleaned = sanitize_resume_text(resume_text)
    joined = " ".join(line.strip() for line in cleaned.splitlines() if line.strip())

    return ParsedResume(
        candidate_name=_extract_name(joined) or _extract_field(joined, "name"),
        email=_extract_field(joined, "email"),
        phone=_extract_field(joined, "phone"),
        linkedin=_extract_field(joined, "linkedin"),
        github=_extract_field(joined, "github"),
        portfolio=_extract_field(joined, "portfolio"),
        education=_extract_section(joined, "education"),
        university=_extract_field(joined, "university"),
        degree=_extract_field(joined, "degree"),
        graduation_year=_extract_field(joined, "graduation year"),
        experience_summary=_extract_section(joined, "experience"),
        companies=_extract_section(joined, "company"),
        roles=_extract_section(joined, "role"),
        duration=_extract_section(joined, "duration"),
        projects=_extract_section(joined, "project"),
        technical_skills=_extract_section(joined, "technical skills"),
        soft_skills=_extract_section(joined, "soft skills"),
        frameworks=_extract_section(joined, "frameworks"),
        programming_languages=_extract_section(joined, "programming languages"),
        cloud_platforms=_extract_section(joined, "cloud"),
        databases=_extract_section(joined, "database"),
        certifications=_extract_section(joined, "certifications"),
        achievements=_extract_section(joined, "achievements"),
        languages=_extract_section(joined, "languages"),
        publications=_extract_section(joined, "publications"),
        volunteer_work=_extract_section(joined, "volunteer"),
    )


def _extract_field(text: str, label: str) -> str:
    return _search_label(text, label)


def _extract_section(text: str, label: str) -> str:
    return _search_label(text, label)


def _search_label(text: str, label: str) -> str:
    if not text:
        return "Not Found"
    lower = text.lower()
    label_lower = label.lower()
    if label_lower not in lower:
        return "Not Found"
    start = lower.find(label_lower)
    excerpt = text[start : start + 300]
    return normalize_not_found(excerpt)


def _extract_name(text: str) -> str:
    match = re.search(r"\b[A-Z][a-z]+\s+[A-Z][a-z]+\b", text)
    if match:
        return match.group(0)
    parts = text.split()
    if len(parts) >= 2:
        return f"{parts[0]} {parts[1]}"
    return "Not Found"
