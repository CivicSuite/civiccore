"""Trusted-header auth helpers for reverse-proxy SSO deployments."""

from __future__ import annotations

import hashlib
from collections.abc import Iterable, Mapping

from fastapi import HTTPException

from civiccore.auth.bearer import AuthenticatedPrincipal


def parse_header_role_list(raw_value: str, *, header_name: str) -> frozenset[str]:
    """Parse a comma-delimited header value into normalized roles."""

    roles = frozenset(role.strip().lower() for role in raw_value.split(",") if role.strip())
    if not roles:
        raise ValueError(f"{header_name} must include at least one non-empty role.")
    return roles


def _lookup_header(headers: Mapping[str, str], header_name: str) -> str | None:
    target = header_name.strip().lower()
    for key, value in headers.items():
        if key.strip().lower() == target:
            candidate = value.strip()
            return candidate or None
    return None


def authorize_trusted_header_roles(
    headers: Mapping[str, str],
    *,
    service_name: str,
    feature_name: str,
    principal_header_name: str,
    roles_header_name: str,
    allowed_roles: Iterable[str],
    provider_name: str = "trusted reverse proxy",
) -> AuthenticatedPrincipal:
    """Validate an asserted principal + roles from a trusted proxy/header bridge."""

    normalized_allowed = frozenset(role.strip().lower() for role in allowed_roles if role.strip())
    if not normalized_allowed:
        raise ValueError("allowed_roles must contain at least one non-empty role.")

    subject = _lookup_header(headers, principal_header_name)
    if subject is None:
        raise HTTPException(
            status_code=401,
            detail={
                "message": "Trusted identity header missing.",
                "fix": (
                    f"Authenticate through the configured {provider_name} flow so it injects "
                    f"{principal_header_name} before CivicClerk handles staff requests."
                ),
            },
        )

    raw_roles = _lookup_header(headers, roles_header_name)
    if raw_roles is None:
        raise HTTPException(
            status_code=401,
            detail={
                "message": "Trusted role header missing.",
                "fix": (
                    f"Configure the trusted proxy to inject {roles_header_name} with one of these "
                    f"roles: {', '.join(sorted(normalized_allowed))}."
                ),
            },
        )

    try:
        header_roles = parse_header_role_list(raw_roles, header_name=roles_header_name)
    except ValueError as exc:
        raise HTTPException(
            status_code=401,
            detail={
                "message": "Trusted role header is invalid.",
                "fix": str(exc),
            },
        ) from exc

    if header_roles.isdisjoint(normalized_allowed):
        raise HTTPException(
            status_code=403,
            detail={
                "message": "Trusted identity lacks an allowed role.",
                "fix": (
                    "Grant the signed-in staff account one of these roles or adjust the "
                    f"{provider_name} role mapping: {', '.join(sorted(normalized_allowed))}."
                ),
                "required_roles": sorted(normalized_allowed),
                "principal_roles": sorted(header_roles),
                "principal": subject,
            },
        )

    return AuthenticatedPrincipal(
        token_fingerprint=hashlib.sha256(subject.encode("utf-8")).hexdigest()[:12],
        roles=header_roles,
        auth_method="trusted_header",
        subject=subject,
        provider=provider_name,
    )


def resolve_optional_trusted_header_roles(
    headers: Mapping[str, str],
    *,
    service_name: str,
    feature_name: str,
    principal_header_name: str,
    roles_header_name: str,
    allowed_roles: Iterable[str],
    provider_name: str = "trusted reverse proxy",
) -> AuthenticatedPrincipal | None:
    """Return an authenticated principal only when trusted headers are present."""

    if _lookup_header(headers, principal_header_name) is None:
        return None

    return authorize_trusted_header_roles(
        headers,
        service_name=service_name,
        feature_name=feature_name,
        principal_header_name=principal_header_name,
        roles_header_name=roles_header_name,
        allowed_roles=allowed_roles,
        provider_name=provider_name,
    )
