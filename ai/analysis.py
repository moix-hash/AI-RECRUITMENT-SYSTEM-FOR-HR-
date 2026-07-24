from __future__ import annotations

import os
import json
from typing import Any, Dict

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableSequence

from ai.prompts import ANALYSIS_PROMPT
from ai.schemas import CandidateAnalysis
from config.settings import GEMINI_API_KEY


class RecruiterAnalyzer:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is required")
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=self.api_key,
            temperature=0.2,
        )
        self.parser = PydanticOutputParser(pydantic_object=CandidateAnalysis)
        self.chain = RunnableSequence(
            ANALYSIS_PROMPT | self.model | self.parser
        )

    def analyze(self, resume_text: str, job_description: str) -> CandidateAnalysis:
        return self.chain.invoke({"resume_text": resume_text, "job_description": job_description})
