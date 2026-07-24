from __future__ import annotations

from typing import Dict


def determine_recommendation(scores: Dict[str, int]) -> str:
    final_score = scores.get("final_score", 0)
    if final_score >= 85:
        return "Strong Hire"
    if final_score >= 70:
        return "Hire"
    if final_score >= 55:
        return "Interview"
    if final_score >= 45:
        return "Hold"
    return "Reject"


def explain_recommendation(scores: Dict[str, int], strengths: list[str], gaps: list[str]) -> str:
    rec = determine_recommendation(scores)
    return (
        f"Recommendation: {rec}. The candidate scored {scores.get('final_score', 0)} out of 100. "
        f"Strengths include {', '.join(strengths[:3]) or 'relevant experience'}. "
        f"Missing areas are {', '.join(gaps[:3]) or 'none detected'}. "
        f"This recommendation is based on technical fit, experience alignment, education relevance, and overall role readiness."
    )
