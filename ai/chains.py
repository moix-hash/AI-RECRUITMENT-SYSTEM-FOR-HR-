from __future__ import annotations

from typing import Any

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableSequence

from ai.llm import LLMFactory
from ai.output_parser import OutputFixingParser
from ai.prompts import JD_ANALYSIS_PROMPT, RESUME_ANALYSIS_PROMPT
from ai.schemas import CandidateAnalysis, ParsedJobDescription, ParsedResume


def build_analysis_chain(llm: Any | None = None) -> RunnableSequence:
    model = llm or LLMFactory().create()
    parser = PydanticOutputParser(pydantic_object=CandidateAnalysis)
    return RunnableSequence(RESUME_ANALYSIS_PROMPT | model | parser)


def build_resume_parser_chain(llm: Any | None = None) -> RunnableSequence:
    model = llm or LLMFactory().create()
    parser = PydanticOutputParser(pydantic_object=ParsedResume)
    return RunnableSequence(RESUME_ANALYSIS_PROMPT | model | parser)


def build_job_parser_chain(llm: Any | None = None) -> RunnableSequence:
    model = llm or LLMFactory().create()
    parser = PydanticOutputParser(pydantic_object=ParsedJobDescription)
    return RunnableSequence(JD_ANALYSIS_PROMPT | model | parser)


class AnalysisChain:
    def __init__(self, llm: Any | None = None) -> None:
        self.llm = llm or LLMFactory().create()
        self.parser = OutputFixingParser(CandidateAnalysis)

    def run_analysis(self, resume_text: str, job_description: str) -> CandidateAnalysis:
        chain = build_analysis_chain(self.llm)
        raw_output = chain.invoke({"resume_text": resume_text, "job_description": job_description})
        return self.parser.parse(str(raw_output))
