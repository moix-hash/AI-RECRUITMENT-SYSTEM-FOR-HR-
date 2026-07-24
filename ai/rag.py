from __future__ import annotations

from typing import List, Optional
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from ai.llm import LLMFactory
from ai.embeddings import EmbeddingService


class RAGService:
    def __init__(self, index: FAISS, chain_type: str = "stuff") -> None:
        self.index = index
        self.chain_type = chain_type
        self.llm = LLMFactory().create()

    def answer(self, query: str, top_k: int = 4) -> str:
        qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type=self.chain_type,
            retriever=self.index.as_retriever(search_kwargs={"k": top_k}),
        )
        return qa.run(query)

    @classmethod
    def create_index(cls, texts: List[str]) -> FAISS:
        return EmbeddingService().build_faiss_index(texts)
