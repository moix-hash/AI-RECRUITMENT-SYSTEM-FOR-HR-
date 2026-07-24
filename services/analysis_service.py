from __future__ import annotations

from typing import Dict

from ai.analysis import RecruiterAnalyzer
from config.settings import GEMINI_API_KEY
from utils.analysis_fallback import build_fallback_analysis


class AnalysisService:
    """Service layer for candidate analysis orchestration."""

    def analyze(self, resume_text: str, job_description: str) -> Dict[str, object]:
        fallback = build_fallback_analysis(resume_text, job_description)
        if not GEMINI_API_KEY:
            return fallback
        try:
            result = RecruiterAnalyzer().analyze(resume_text, job_description).model_dump()
            fallback.update(
                {
                    "candidate_summary": result.get("professional_summary") or fallback["candidate_summary"],
                    "experience_summary": result.get("experience_analysis") or fallback["experience_summary"],
                    "education_summary": result.get("education_analysis") or fallback["education_summary"],
                    "project_summary": result.get("project_analysis") or fallback["project_summary"],
                    "matching_skills": result.get("matching_skills") or fallback["matching_skills"],
                    "missing_skills": result.get("missing_skills") or fallback["missing_skills"],
                    "extra_skills": result.get("extra_skills") or fallback["extra_skills"],
                    "recommendation": result.get("recommendation") or fallback["recommendation"],
                    "justification": result.get("recommendation_justification") or fallback["justification"],
                    "interview_questions": result.get("interview_questions") or fallback["interview_questions"],
                    "final_score": result.get("final_score") if result.get("final_score") is not None else fallback["final_score"],
                    "analysis_mode": "Gemini via LangChain",
                }
            )
        except Exception:
            # The app remains useful if the configured model is unavailable, rate-limited,
            # or returns malformed structured output.
            fallback["analysis_mode"] = "Local fallback (Gemini unavailable)"
        return fallback
