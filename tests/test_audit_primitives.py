"""Tests for hash-chained audit primitives."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from civiccore.audit import (
    AuditActor,
    AuditEvent,
    AuditHashChain,
    AuditSubject,
    record_event,
    verify_chain,
)


def _actor() -> AuditActor:
    return AuditActor(actor_id="user-123", actor_type="staff", display_name="Case Worker")


def _subject() -> AuditSubject:
    return AuditSubject(subject_id="record-456", subject_type="records_request")


def test_record_event_builds_verifiable_hash_chain() -> None:
    first = record_event(
        actor=_actor(),
        action="created",
        subject=_subject(),
        source_module="records",
        timestamp=datetime(2026, 4, 1, 12, 0, tzinfo=UTC),
        metadata={"request_number": "RR-1"},
    )
    second = record_event(
        [first],
        actor=_actor(),
        action="classified",
        subject=_subject(),
        source_module="records",
        timestamp=datetime(2026, 4, 1, 12, 5, tzinfo=UTC),
        metadata={"exemption_codes": ["draft"]},
    )

    assert first.previous_hash is None
    assert second.previous_hash == first.current_hash
    assert verify_chain([first, second])


def test_verify_chain_detects_modified_payload_without_rehash() -> None:
    chain = AuditHashChain()
    event = chain.record_event(
        actor=_actor(),
        action="exported",
        subject=_subject(),
        source_module="exports",
        timestamp=datetime(2026, 4, 1, 13, 0, tzinfo=UTC),
        metadata={"format": "pdf"},
    )

    tampered = event.model_copy(update={"metadata": {"format": "docx"}})

    assert event.current_hash == chain.events[0].current_hash
    assert not verify_chain([tampered])


def test_verify_chain_detects_missing_middle_event_broken_link() -> None:
    chain = AuditHashChain()
    base_time = datetime(2026, 4, 1, 14, 0, tzinfo=UTC)
    chain.record_event(
        actor=_actor(),
        action="created",
        subject=_subject(),
        source_module="records",
        timestamp=base_time,
    )
    chain.record_event(
        actor=_actor(),
        action="reviewed",
        subject=_subject(),
        source_module="records",
        timestamp=base_time + timedelta(minutes=1),
    )
    chain.record_event(
        actor=_actor(),
        action="released",
        subject=_subject(),
        source_module="records",
        timestamp=base_time + timedelta(minutes=2),
    )

    assert chain.verify()
    assert not verify_chain([chain.events[0], chain.events[2]])


def test_verify_chain_detects_broken_previous_hash() -> None:
    chain = AuditHashChain()
    first = chain.record_event(
        actor=_actor(),
        action="created",
        subject=_subject(),
        source_module="records",
        timestamp=datetime(2026, 4, 1, 15, 0, tzinfo=UTC),
    )
    second = chain.record_event(
        actor=_actor(),
        action="updated",
        subject=_subject(),
        source_module="records",
        timestamp=datetime(2026, 4, 1, 15, 1, tzinfo=UTC),
    )
    broken = second.model_copy(update={"previous_hash": "not-the-first-hash"})

    assert first.current_hash is not None
    assert not verify_chain([first, broken])


def test_audit_event_rejects_naive_timestamps() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        AuditEvent(
            actor=_actor(),
            action="created",
            subject=_subject(),
            source_module="records",
            timestamp=datetime(2026, 4, 1, 12, 0),
        )
