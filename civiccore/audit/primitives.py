"""Hash-chained audit primitives for CivicCore.

The primitives in this module are intentionally storage-neutral: callers can
persist the Pydantic models in SQLAlchemy, files, queues, or keep them in
memory while still getting deterministic tamper checks.
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from typing import Any, Iterable, Sequence
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _require_timezone(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("timestamp must be timezone-aware")
    return value


def _canonicalize(value: Any) -> Any:
    """Convert Pydantic/python values into deterministic JSON-ready values."""

    if isinstance(value, BaseModel):
        return _canonicalize(value.model_dump(mode="python"))
    if isinstance(value, datetime):
        return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
    if isinstance(value, dict):
        return {str(key): _canonicalize(value[key]) for key in sorted(value)}
    if isinstance(value, (list, tuple)):
        return [_canonicalize(item) for item in value]
    return value


def _canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(
        _canonicalize(payload),
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    )


class AuditActor(BaseModel):
    """Actor that initiated an auditable action."""

    model_config = ConfigDict(extra="forbid")

    actor_id: str
    actor_type: str
    display_name: str | None = None


class AuditSubject(BaseModel):
    """Record, document, workflow, or other entity affected by an action."""

    model_config = ConfigDict(extra="forbid")

    subject_id: str
    subject_type: str
    display_name: str | None = None


class AuditEvent(BaseModel):
    """One audit event with deterministic hash-chain fields."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    event_id: str = Field(default_factory=lambda: str(uuid4()))
    actor: AuditActor
    action: str
    subject: AuditSubject
    source_module: str
    timestamp: datetime = Field(default_factory=_utc_now)
    metadata: dict[str, Any] = Field(default_factory=dict)
    previous_hash: str | None = None
    current_hash: str | None = None

    @field_validator("timestamp")
    @classmethod
    def _timestamp_must_be_aware(cls, value: datetime) -> datetime:
        return _require_timezone(value)

    def hash_payload(self) -> dict[str, Any]:
        """Return the payload covered by ``current_hash``."""

        return self.model_dump(mode="python", exclude={"current_hash"})

    def compute_hash(self) -> str:
        """Compute the SHA-256 hash of the canonical event payload."""

        return hashlib.sha256(_canonical_json(self.hash_payload()).encode("utf-8")).hexdigest()

    def seal(self) -> "AuditEvent":
        """Return a copy whose ``current_hash`` matches its payload."""

        return self.model_copy(update={"current_hash": self.compute_hash()})


def _last_hash(events: Sequence[AuditEvent] | "AuditHashChain" | None) -> str | None:
    if events is None:
        return None
    chain_events = events.events if isinstance(events, AuditHashChain) else events
    if not chain_events:
        return None
    return chain_events[-1].current_hash


def record_event(
    events: Sequence[AuditEvent] | "AuditHashChain" | None = None,
    *,
    actor: AuditActor,
    action: str,
    subject: AuditSubject,
    source_module: str,
    timestamp: datetime | None = None,
    metadata: dict[str, Any] | None = None,
) -> AuditEvent:
    """Create and seal an audit event linked to the prior event, if any."""

    event = AuditEvent(
        actor=actor,
        action=action,
        subject=subject,
        source_module=source_module,
        timestamp=timestamp or _utc_now(),
        metadata=metadata or {},
        previous_hash=_last_hash(events),
    )
    return event.seal()


def verify_chain(events: Iterable[AuditEvent]) -> bool:
    """Return ``True`` only when hashes and previous links are intact."""

    previous_hash: str | None = None
    for event in events:
        if event.current_hash is None:
            return False
        if event.previous_hash != previous_hash:
            return False
        if event.compute_hash() != event.current_hash:
            return False
        previous_hash = event.current_hash
    return True


class AuditHashChain(BaseModel):
    """In-memory helper for building and verifying hash-chained events."""

    model_config = ConfigDict(extra="forbid")

    events: list[AuditEvent] = Field(default_factory=list)

    def record_event(
        self,
        *,
        actor: AuditActor,
        action: str,
        subject: AuditSubject,
        source_module: str,
        timestamp: datetime | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> AuditEvent:
        event = record_event(
            self.events,
            actor=actor,
            action=action,
            subject=subject,
            source_module=source_module,
            timestamp=timestamp,
            metadata=metadata,
        )
        self.events.append(event)
        return event

    def verify(self) -> bool:
        return verify_chain(self.events)


__all__ = [
    "AuditActor",
    "AuditEvent",
    "AuditHashChain",
    "AuditSubject",
    "record_event",
    "verify_chain",
]
