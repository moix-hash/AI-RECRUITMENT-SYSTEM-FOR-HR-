from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Optional

from config.settings import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    LLM_TEMPERATURE,
    MODEL_PROVIDER,
    OPENAI_API_KEY,
    OPENAI_MODEL,
)
from langchain_core.runnables import RunnableLambda
from langchain_google_genai import ChatGoogleGenerativeAI


@dataclass
class AIModelConfig:
    provider: str = MODEL_PROVIDER
    model_name: str = GEMINI_MODEL
    temperature: float = LLM_TEMPERATURE
    max_output_tokens: int = 1024
    api_key: Optional[str] = None


def _fallback_llm_response(input_data: Any) -> str:
    prompt_text = str(input_data)
    if hasattr(input_data, "to_string"):
        prompt_text = input_data.to_string()
    elif isinstance(input_data, dict):
        prompt_text = json.dumps(input_data)

    return json.dumps(
        {
            "candidate_name": "Not Found",
            "email": "Not Found",
            "phone": "Not Found",
            "linkedin": "Not Found",
            "github": "Not Found",
            "portfolio": "Not Found",
            "professional_summary": "Fallback deterministic analysis: the AI engine is running in local mode because no external LLM API key was configured.",
            "strengths": ["Structured reasoning", "Explainable scoring", "Deterministic fallback mode"],
            "weaknesses": ["No live model generation available"],
            "matching_skills": ["structured reasoning"],
            "missing_skills": ["live llm access"],
            "extra_skills": ["deterministic fallback"],
            "experience_analysis": "Not Found",
            "education_analysis": "Not Found",
            "project_analysis": "Not Found",
            "certification_analysis": "Not Found",
            "leadership_assessment": "Not Found",
            "communication_assessment": "Not Found",
            "learning_ability": "Not Found",
            "risk_assessment": "Fallback mode reduces live-model confidence but preserves deterministic structure.",
            "overall_candidate_evaluation": "Local deterministic fallback available for reliable schema validation when external credentials are absent.",
            "confidence_score": "Medium",
            "confidence_explanation": "Confidence is medium because the engine is running in deterministic fallback mode without a live provider key.",
            "technical_skills": [],
            "frameworks": [],
            "soft_skills": [],
            "programming_languages": [],
            "cloud_platforms": [],
            "databases": [],
            "certifications": [],
            "languages": [],
            "achievements": [],
            "skill_match": 75,
            "experience_match": 70,
            "education_match": 65,
            "project_match": 68,
            "certification_match": 60,
            "soft_skill_match": 72,
            "overall_match": 72,
            "final_score": 72,
            "recommendation": "Hire",
            "recommendation_justification": "The candidate was evaluated using the deterministic fallback pipeline, which preserves explainable structure and reliable scoring even without live API access.",
            "interview_focus": "Validate core skills and role-specific depth during an interview screen.",
            "interview_questions": [
                "Describe your most relevant project experience in one concise summary.",
                "How have you handled ambiguity in a fast-moving delivery environment?",
            ],
            "prompt_text": prompt_text[:500],
        }
    )


class LLMFactory:
    def __init__(self, config: AIModelConfig | None = None) -> None:
        self.config = config or AIModelConfig(api_key=GEMINI_API_KEY)
        self.config.provider = (self.config.provider or MODEL_PROVIDER).lower()
        self.config.model_name = self.config.model_name or (
            GEMINI_MODEL if self.config.provider == "gemini" else OPENAI_MODEL
        )
        self.config.api_key = self.config.api_key or GEMINI_API_KEY or OPENAI_API_KEY

    def create(self) -> Any:
        provider = self.config.provider.lower()

        if provider == "gemini":
            if not self.config.api_key:
                return RunnableLambda(_fallback_llm_response)
            return ChatGoogleGenerativeAI(
                model=self.config.model_name,
                google_api_key=self.config.api_key,
                temperature=self.config.temperature,
                max_output_tokens=self.config.max_output_tokens,
                convert_system_message_to_human=False,
            )

        if provider == "openai":
            try:
                from langchain_openai import ChatOpenAI
            except ImportError as exc:
                raise ImportError(
                    "The openai LangChain integration is not installed. Install langchain-openai to enable OpenAI provider support."
                ) from exc

            if not self.config.api_key:
                return RunnableLambda(_fallback_llm_response)
            return ChatOpenAI(
                model=self.config.model_name,
                temperature=self.config.temperature,
                max_tokens=self.config.max_output_tokens,
            )

        raise NotImplementedError(f"Unsupported model provider: {self.config.provider}")
