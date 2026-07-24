from __future__ import annotations

from typing import Any, Dict

WEIGHTS = {
    "technical_skills": 0.40,
    "experience": 0.25,
    "projects": 0.15,
    "education": 0.10,
    "certifications": 0.05,
    "soft_skills": 0.05,
}


def calculate_weighted_score(metrics: Dict[str, int]) -> int:
    total = 0.0
    for category, weight in WEIGHTS.items():
        total += metrics.get(category, 0) * weight
    return min(100, max(0, int(round(total))))


def rank_candidates(candidates: list[Dict[str, Any]]) -> list[Dict[str, Any]]:
    ranked = sorted(
        candidates,
        key=lambda item: (
            item.get("final_score", 0),
            item.get("confidence_score", 0),
            item.get("skill_match", 0),
        ),
        reverse=True,
    )
    for index, candidate in enumerate(ranked, start=1):
        candidate["rank"] = index
    return ranked
