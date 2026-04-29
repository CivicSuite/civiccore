"""Shared ingest contracts for current CivicSuite consumers.

This package intentionally ships the smallest honest reusable ingest surface:
connector discovery/fetch contracts plus cited-source validation primitives for
LLM-assisted drafts and other document-derived workflows.
"""

from civiccore.ingest.contracts import (
    CitedSentence,
    CitationValidationError,
    DiscoveredRecord,
    FetchedDocument,
    HealthCheckResult,
    HealthStatus,
    SourceMaterial,
    validate_cited_sentences,
)

__all__ = [
    "CitedSentence",
    "CitationValidationError",
    "DiscoveredRecord",
    "FetchedDocument",
    "HealthCheckResult",
    "HealthStatus",
    "SourceMaterial",
    "validate_cited_sentences",
]
