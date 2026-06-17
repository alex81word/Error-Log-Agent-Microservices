from __future__ import annotations

import os

from langchain_openai import ChatOpenAI


def create_chat_model(*, model: str | None = None, temperature: float = 0.0) -> ChatOpenAI:
    """Build the LangChain OpenAI chat model used by the analyzer."""

    return ChatOpenAI(
        model=model or os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        temperature=temperature,
    )

