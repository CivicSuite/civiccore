"""Ollama local LLM runtime provider.

Uses httpx (already a civiccore dependency — no extra packages required) to
talk to a local Ollama daemon over its HTTP API.

Default generation model is ``gemma4:e4b``, which matches the current
records-ai production default. Default embedding model is
``nomic-embed-text``.

Note: Ollama's embeddings endpoint accepts a single ``prompt`` per request,
so :meth:`OllamaProvider.embed_batch` loops sequentially. Parallel batching
is a v0.3.0 candidate; records-ai today does the same.
"""

from __future__ import annotations

import httpx

from civiccore.llm.providers.base import LLMProvider
from civiccore.llm.providers.registry import register_provider


@register_provider("ollama")
class OllamaProvider(LLMProvider):
    """Ollama local LLM runtime provider.

    Talks to a local Ollama daemon at ``base_url`` (default
    ``http://localhost:11434``). Default model is ``gemma4:e4b``
    (records-ai's current production default). Supports both text and
    multimodal (images via base64) generation.
    """

    def __init__(
        self,
        *,
        base_url: str = "http://localhost:11434",
        default_model: str = "gemma4:e4b",
        default_embed_model: str = "nomic-embed-text",
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.default_model = default_model
        self.default_embed_model = default_embed_model

    @property
    def name(self) -> str:
        return "ollama"

    @property
    def supports_images(self) -> bool:
        return True

    async def generate(
        self,
        *,
        system_prompt: str,
        user_content: str,
        model: str | None = None,
        chunks: list[str] | None = None,
        exemption_rules: list[str] | None = None,
        images: list[str] | None = None,
        timeout: float = 120.0,
    ) -> str:
        model = model or self.default_model
        # Compose user prompt: chunks + exemption rules + main content
        parts: list[str] = []
        if chunks:
            parts.append("\n\n".join(chunks))
        if exemption_rules:
            parts.append("Exemption rules:\n" + "\n".join(exemption_rules))
        parts.append(user_content)
        prompt = "\n\n".join(parts)

        payload: dict = {
            "model": model,
            "system": system_prompt,
            "prompt": prompt,
            "stream": False,
        }
        if images:
            payload["images"] = images

        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(f"{self.base_url}/api/generate", json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data.get("response", "")

    async def embed(self, text: str, *, model: str | None = None) -> list[float]:
        model = model or self.default_embed_model
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                f"{self.base_url}/api/embeddings",
                json={"model": model, "prompt": text},
            )
            resp.raise_for_status()
            data = resp.json()
            return list(data.get("embedding", []))

    async def embed_batch(
        self,
        texts: list[str],
        *,
        model: str | None = None,
    ) -> list[list[float]]:
        # Ollama's embeddings API is single-text; loop sequentially.
        # Records-ai today does the same; batch parallelism is a v0.3.0 candidate.
        results: list[list[float]] = []
        for text in texts:
            results.append(await self.embed(text, model=model))
        return results


__all__ = ["OllamaProvider"]
