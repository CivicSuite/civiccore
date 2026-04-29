"""Small shared search helpers for current CivicSuite consumers.

This package intentionally ships the smallest honest cross-module surface:
query/text normalization for deterministic substring matching and a generic
reciprocal-rank-fusion helper for hybrid search result merging.
"""

from __future__ import annotations

from collections.abc import Hashable, Sequence
from typing import TypeVar


SearchResultId = TypeVar("SearchResultId", bound=Hashable)


def normalize_search_text(text: str) -> str:
    """Normalize search text for case-insensitive, whitespace-stable matching."""
    return " ".join(text.split()).strip().lower()


def normalize_search_query(query: str) -> str:
    """Normalize a free-text query using the same rules as searchable content."""
    return normalize_search_text(query)


def search_text_matches_query(*, text: str, query: str) -> bool:
    """Return True when the normalized query appears in normalized text."""
    normalized_query = normalize_search_query(query)
    if not normalized_query:
        return True
    return normalized_query in normalize_search_text(text)


def reciprocal_rank_fusion(
    semantic_results: Sequence[tuple[SearchResultId, float]],
    keyword_results: Sequence[tuple[SearchResultId, float]],
    *,
    k: int = 60,
    semantic_weight: float = 0.7,
    keyword_weight: float = 0.3,
) -> list[tuple[SearchResultId, float]]:
    """Fuse semantic and keyword rankings into one weighted result list."""
    scores: dict[SearchResultId, float] = {}

    for rank, (result_id, _) in enumerate(semantic_results):
        scores[result_id] = scores.get(result_id, 0.0) + semantic_weight / (k + rank + 1)

    for rank, (result_id, _) in enumerate(keyword_results):
        scores[result_id] = scores.get(result_id, 0.0) + keyword_weight / (k + rank + 1)

    return sorted(scores.items(), key=lambda item: item[1], reverse=True)


__all__ = [
    "normalize_search_query",
    "normalize_search_text",
    "reciprocal_rank_fusion",
    "search_text_matches_query",
]
