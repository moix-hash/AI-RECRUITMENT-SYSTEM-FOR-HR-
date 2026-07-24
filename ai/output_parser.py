from __future__ import annotations

import json
import re
from typing import Any, Type

from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, ValidationError


class StrictPydanticParser:
    def __init__(self, model: Type[BaseModel]) -> None:
        self.parser = PydanticOutputParser(pydantic_object=model)

    def parse(self, text: str | BaseModel) -> BaseModel:
        if isinstance(text, BaseModel):
            return text
        normalized = self._normalize_payload(text)
        try:
            return self.parser.parse(normalized)
        except ValidationError as exc:
            raise ValueError(f"AI output validation failed: {exc}") from exc

    def parse_with_retry(self, text: str, retries: int = 2) -> BaseModel:
        for attempt in range(retries + 1):
            try:
                return self.parse(text)
            except ValueError:
                if attempt == retries:
                    raise
                text = self._repair_text(text)
        raise ValueError("AI output could not be repaired into a valid schema")

    def format(self, obj: Any) -> str:
        return self.parser.format(obj)

    def _normalize_payload(self, text: str) -> str:
        if not isinstance(text, str):
            return str(text)
        text = text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
            text = re.sub(r"\s*```$", "", text, flags=re.IGNORECASE)
        return text

    def _repair_text(self, text: str) -> str:
        cleaned = self._normalize_payload(text)
        match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
        if match:
            return match.group(0)
        try:
            parsed = json.loads(cleaned)
            return json.dumps(parsed)
        except Exception:
            return cleaned


class OutputFixingParser:
    def __init__(self, model: Type[BaseModel]) -> None:
        self.strict_parser = StrictPydanticParser(model)

    def parse(self, text: str) -> BaseModel:
        return self.strict_parser.parse_with_retry(text)

    def format(self, obj: Any) -> str:
        return self.strict_parser.format(obj)
