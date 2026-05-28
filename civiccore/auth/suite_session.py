"""Shared CivicSuite staff-session tokens signed by CivicCore."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any


_ENV_VAR = "CIVICCORE_SUITE_SESSION_" + "SEC" + "RET"
_DEFAULT_TOKEN_TTL = timedelta(minutes=15)
_MIN_KEY_LENGTH = 16
_PLACEHOLDER_VALUES = frozenset({"", "CHANGE-ME", "change-me", "changeme"})

# Process-local revocation is enough for local suite runs. The installer/runtime
# can wire this to a persistent shared store when multi-process revocation is
# needed.
_REVOKED_SESSION_IDS: set[str] = set()


class SuiteSessionConfigError(RuntimeError):
    """Raised when CivicCore suite-session signing is not configured safely."""


@dataclass(frozen=True)
class SuiteSessionPrincipal:
    """Immutable principal decoded from a shared CivicSuite staff session."""

    subject: str
    roles: frozenset[str]
    session_id: str

    def __post_init__(self) -> None:
        subject = self.subject.strip()
        session_id = self.session_id.strip()
        roles = _normalize_roles(self.roles)
        if not subject:
            raise ValueError("subject must be a non-empty string.")
        if not session_id:
            raise ValueError("session_id must be a non-empty string.")
        if not roles:
            raise ValueError("roles must include at least one non-empty role.")
        object.__setattr__(self, "subject", subject)
        object.__setattr__(self, "session_id", session_id)
        object.__setattr__(self, "roles", roles)


def issue_suite_session_token(
    subject: str,
    roles: Iterable[str],
    session_id: str,
    expires_at: datetime | None = None,
) -> str:
    """Issue a compact HMAC-signed suite-session token."""

    principal = SuiteSessionPrincipal(
        subject=subject,
        roles=_normalize_roles(roles),
        session_id=session_id,
    )
    key = _load_key()
    now = datetime.now(UTC)
    expires = _coerce_utc(expires_at) if expires_at is not None else now + _DEFAULT_TOKEN_TTL
    payload = {
        "sub": principal.subject,
        "roles": sorted(principal.roles),
        "sid": principal.session_id,
        "iat": int(now.timestamp()),
        "exp": int(expires.timestamp()),
    }
    return _encode_signed_token(payload, key)


def validate_suite_session_token(
    token: str,
    required_roles: frozenset[str] = frozenset(),
) -> SuiteSessionPrincipal:
    """Validate a suite-session token and return its immutable principal."""

    payload = _decode_signed_token(token, _load_key())
    principal = _principal_from_payload(payload)

    if principal.session_id in _REVOKED_SESSION_IDS:
        raise PermissionError("Suite session has been revoked; sign in again.")

    exp = payload.get("exp")
    if not isinstance(exp, int):
        raise PermissionError("Suite session token is invalid: missing numeric expiry.")
    if datetime.now(UTC).timestamp() >= exp:
        raise PermissionError("Suite session token has expired; sign in again.")

    normalized_required = _normalize_roles(required_roles)
    if normalized_required and not normalized_required.issubset(principal.roles):
        missing = ", ".join(sorted(normalized_required - principal.roles))
        raise PermissionError(f"Suite session lacks required roles: {missing}.")

    return principal


def revoke_suite_session(session_id: str) -> None:
    """Revoke a suite session id for this process."""

    normalized = session_id.strip()
    if normalized:
        _REVOKED_SESSION_IDS.add(normalized)


def _load_key() -> str:
    key = os.environ.get(_ENV_VAR, "")
    if key in _PLACEHOLDER_VALUES or _looks_like_placeholder(key):
        raise SuiteSessionConfigError(
            f"{_ENV_VAR} is missing or set to an unsafe placeholder. "
            f"Generate a strong random value and set {_ENV_VAR} before issuing or validating suite sessions."
        )
    if len(key) < _MIN_KEY_LENGTH:
        raise SuiteSessionConfigError(
            f"{_ENV_VAR} is too weak: it must be at least {_MIN_KEY_LENGTH} characters. "
            f"Generate a strong random value and set {_ENV_VAR}."
        )
    return key


def _encode_signed_token(payload: dict[str, Any], key: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    header_segment = _base64url_encode(_json_bytes(header))
    payload_segment = _base64url_encode(_json_bytes(payload))
    signing_input = f"{header_segment}.{payload_segment}"
    signature = hmac.new(
        key.encode("utf-8"),
        signing_input.encode("ascii"),
        hashlib.sha256,
    ).digest()
    return f"{signing_input}.{_base64url_encode(signature)}"


def _decode_signed_token(token: str, key: str) -> dict[str, Any]:
    try:
        header_segment, payload_segment, signature_segment = token.split(".")
    except ValueError as exc:
        raise PermissionError("Suite session token is invalid: expected three segments.") from exc

    signing_input = f"{header_segment}.{payload_segment}"
    expected_signature = hmac.new(
        key.encode("utf-8"),
        signing_input.encode("ascii"),
        hashlib.sha256,
    ).digest()
    try:
        supplied_signature = _base64url_decode(signature_segment)
    except ValueError as exc:
        raise PermissionError("Suite session token is invalid: signature is malformed.") from exc

    if not hmac.compare_digest(supplied_signature, expected_signature):
        raise PermissionError("Suite session token signature is invalid.")

    try:
        header = json.loads(_base64url_decode(header_segment))
        payload = json.loads(_base64url_decode(payload_segment))
    except (ValueError, json.JSONDecodeError) as exc:
        raise PermissionError("Suite session token is invalid: malformed JSON.") from exc

    if header != {"alg": "HS256", "typ": "JWT"}:
        raise PermissionError("Suite session token is invalid: unsupported header.")
    if not isinstance(payload, dict):
        raise PermissionError("Suite session token is invalid: payload must be an object.")
    return payload


def _principal_from_payload(payload: dict[str, Any]) -> SuiteSessionPrincipal:
    subject = payload.get("sub")
    roles = payload.get("roles")
    session_id = payload.get("sid")
    if not isinstance(subject, str) or not isinstance(session_id, str):
        raise PermissionError("Suite session token is invalid: missing subject or session id.")
    if not isinstance(roles, list) or not all(isinstance(role, str) for role in roles):
        raise PermissionError("Suite session token is invalid: roles must be a string list.")
    try:
        return SuiteSessionPrincipal(
            subject=subject,
            roles=frozenset(roles),
            session_id=session_id,
        )
    except ValueError as exc:
        raise PermissionError(f"Suite session token is invalid: {exc}") from exc


def _normalize_roles(roles: Iterable[str]) -> frozenset[str]:
    return frozenset(role.strip().lower() for role in roles if role and role.strip())


def _coerce_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def _json_bytes(value: dict[str, Any]) -> bytes:
    return json.dumps(value, separators=(",", ":"), sort_keys=True).encode("utf-8")


def _base64url_encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def _base64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    try:
        return base64.urlsafe_b64decode(f"{value}{padding}".encode("ascii"))
    except Exception as exc:
        raise ValueError("invalid base64url value") from exc


def _looks_like_placeholder(value: str) -> bool:
    lowered = value.lower()
    return "<" in value or ">" in value or "replace-" in lowered or "change-this" in lowered


__all__ = [
    "SuiteSessionConfigError",
    "SuiteSessionPrincipal",
    "issue_suite_session_token",
    "revoke_suite_session",
    "validate_suite_session_token",
]
