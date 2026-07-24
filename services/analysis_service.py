from __future__ import annotations

from typing import Dict

from utils.analysis_fallback import build_fallback_analysis


class AnalysisService:
    """Service layer for candidate analysis orchestration."""

    def analyze(self, resume_text: str, job_description: str) -> Dict[str, object]:
        return build_fallback_analysis(resume_text, job_description)
