from __future__ import annotations

from typing import Any

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from config.settings import OPENAI_API_KEY


class EmbeddingService:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API key is required for embeddings")
        self.model = "text-embedding-3-small"

    def create_embedding(self, text: str) -> list[float]:
        embed = OpenAIEmbeddings(openai_api_key=self.api_key, model=self.model)
        return embed.embed_query(text)

    def build_faiss_index(self, texts: list[str]) -> FAISS:
        embed = OpenAIEmbeddings(openai_api_key=self.api_key, model=self.model)
        vectors = [embed.embed_query(text) for text in texts]
        return FAISS.from_vectors(vectors, texts)
