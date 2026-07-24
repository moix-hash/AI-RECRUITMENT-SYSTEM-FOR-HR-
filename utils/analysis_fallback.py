from __future__ import annotations

import re
from typing import Dict, List


SKILL_KEYWORDS = (
    "python", "fastapi", "django", "sql", "postgresql", "aws", "azure", "gcp", "docker", "kubernetes",
    "terraform", "linux", "react", "typescript", "javascript", "node", "java", "spring", "kafka",
    "pytorch", "machine learning", "mlops", "llm", "rag", "langchain", "api", "apis", "graphql",
    "data analysis", "tableau", "power bi", "product management", "customer support", "operations",
    "business development", "fraud investigation", "recovery", "communication", "leadership",
)


def _skills_in(text: str) -> set[str]:
    lowered = text.lower()
    return {skill for skill in SKILL_KEYWORDS if re.search(rf"(?<![a-z]){re.escape(skill)}(?![a-z])", lowered)}


def build_fallback_analysis(resume_text: str, job_description: str) -> Dict[str, object]:
    resume_skills = _skills_in(resume_text)
    job_skills = _skills_in(job_description)
    matching_skills = sorted(resume_skills & job_skills)[:8]
    missing_skills = sorted(job_skills - resume_skills)[:8]
    extra_skills = sorted(resume_skills - job_skills)[:8]
    score = min(100, max(20, 38 + len(matching_skills) * 12 - len(missing_skills) * 5 + min(len(extra_skills), 3) * 2))
    if score >= 85:
        recommendation = "Strong Hire"
    elif score >= 75:
        recommendation = "Hire"
    elif score >= 60:
        recommendation = "Interview"
    elif score >= 40:
        recommendation = "Hold"
    else:
        recommendation = "Reject"

    strength_text = ", ".join(matching_skills[:3]) or "transferable professional experience"
    gap_text = ", ".join(missing_skills[:3]) or "no major keyword gaps"
    primary_match = matching_skills[0] if matching_skills else "the role requirements"
    first_gap = missing_skills[0] if missing_skills else "relevant delivery outcomes"

    return {
        "candidate_summary": f"This CV shows evidence of {strength_text}. The main area(s) to validate for this role: {gap_text}.",
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "extra_skills": extra_skills,
        "recommendation": recommendation,
        "final_score": score,
        "interview_questions": [
            f"Tell us about a project where you used {primary_match} and what outcome you achieved.",
            f"How would you close the gap in {first_gap} for this role?",
        ],
    }
