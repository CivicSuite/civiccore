"""Embedding helpers for the shared CivicCore ingestion pipeline."""

from __future__ import annotations

from civiccore.llm.providers import OllamaProvider

_provider: OllamaProvider | None = None


def _get_provider(base_url: str = "http://localhost:11434") -> OllamaProvider:
    global _provider
    if _provider is None:
        _provider = OllamaProvider(base_url=base_url, default_model="gemma4:e4b")
    return _provider


async def embed_text(
    text: str,
    model: str = "nomic-embed-text",
    *,
    base_url: str = "http://localhost:11434",
) -> list[float]:
    """Embed one text string with the local Ollama embedding model."""

    provider = _get_provider(base_url=base_url)
    return await provider.embed(text, model=model)


async def embed_batch(
    texts: list[str],
    model: str = "nomic-embed-text",
    *,
    base_url: str = "http://localhost:11434",
    batch_size: int = 8,
) -> list[list[float]]:
    """Embed a batch of text strings with the local Ollama embedding model."""

    if not texts:
        return []
    provider = _get_provider(base_url=base_url)
    embeddings: list[list[float]] = []
    for start in range(0, len(texts), batch_size):
        batch = texts[start : start + batch_size]
        embeddings.extend(await provider.embed_batch(batch, model=model))
    return embeddings


__all__ = ["embed_batch", "embed_text"]
