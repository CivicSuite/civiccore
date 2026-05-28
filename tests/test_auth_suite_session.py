"""Contract tests for CivicCore-owned suite staff session tokens."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from civiccore.auth.suite_session import (
    SuiteSessionConfigError,
    SuiteSessionPrincipal,
    issue_suite_session_token,
    revoke_suite_session,
    validate_suite_session_token,
)


def test_suite_session_token_validates_role_claims_and_rejects_revocation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CIVICCORE_SUITE_SESSION_SECRET", "test-secret-with-enough-entropy")
    expires_at = datetime.now(UTC) + timedelta(minutes=15)

    token = issue_suite_session_token(
        subject="admin@example.gov",
        roles=frozenset({"records_admin", "clerk_admin", "code_admin"}),
        session_id="suite-session-123",
        expires_at=expires_at,
    )

    principal = validate_suite_session_token(
        token,
        required_roles=frozenset({"records_admin"}),
    )

    assert principal == SuiteSessionPrincipal(
        subject="admin@example.gov",
        roles=frozenset({"records_admin", "clerk_admin", "code_admin"}),
        session_id="suite-session-123",
    )

    revoke_suite_session("suite-session-123")

    with pytest.raises(PermissionError, match="revoked"):
        validate_suite_session_token(token, required_roles=frozenset({"records_admin"}))


def test_suite_session_secret_is_required_with_actionable_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CIVICCORE_SUITE_SESSION_SECRET", raising=False)

    with pytest.raises(SuiteSessionConfigError, match="CIVICCORE_SUITE_SESSION_SECRET"):
        issue_suite_session_token(
            subject="admin@example.gov",
            roles=frozenset({"records_admin"}),
            session_id="suite-session-missing-secret",
        )
