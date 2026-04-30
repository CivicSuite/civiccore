from __future__ import annotations

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from civiccore.auth import (
    AuthenticatedPrincipal,
    authorize_bearer_roles,
    authorize_trusted_header_roles,
    parse_header_role_list,
    parse_token_role_map,
    resolve_optional_bearer_roles,
    resolve_optional_trusted_header_roles,
)


def test_parse_token_role_map_accepts_string_and_list_roles() -> None:
    parsed = parse_token_role_map(
        '{"reader-token": "workpaper_reader, budget_admin", "admin-token": ["records_admin"]}',
        env_var="CIVIC_TEST_AUTH_TOKEN_ROLES",
    )

    assert parsed == {
        "reader-token": frozenset({"workpaper_reader", "budget_admin"}),
        "admin-token": frozenset({"records_admin"}),
    }


def test_parse_token_role_map_rejects_invalid_json() -> None:
    with pytest.raises(ValueError, match="valid JSON"):
        parse_token_role_map("{not-json}", env_var="CIVIC_TEST_AUTH_TOKEN_ROLES")


def test_authorize_bearer_roles_requires_config(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CIVIC_TEST_AUTH_TOKEN_ROLES", raising=False)

    with pytest.raises(HTTPException) as exc_info:
        authorize_bearer_roles(
            None,
            service_name="CivicBudget",
            feature_name="persisted workpaper retrieval",
            token_roles_env_var="CIVIC_TEST_AUTH_TOKEN_ROLES",
            allowed_roles={"workpaper_reader"},
        )

    assert exc_info.value.status_code == 503
    assert exc_info.value.detail["message"] == (
        "CivicBudget persisted workpaper retrieval auth is not configured."
    )
    assert "Set CIVIC_TEST_AUTH_TOKEN_ROLES" in exc_info.value.detail["fix"]


def test_authorize_bearer_roles_rejects_missing_bearer_header(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CIVIC_TEST_AUTH_TOKEN_ROLES", '{"reader-token": ["workpaper_reader"]}')

    with pytest.raises(HTTPException) as exc_info:
        authorize_bearer_roles(
            None,
            service_name="CivicBudget",
            feature_name="persisted workpaper retrieval",
            token_roles_env_var="CIVIC_TEST_AUTH_TOKEN_ROLES",
            allowed_roles={"workpaper_reader"},
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.headers == {"WWW-Authenticate": "Bearer"}
    assert exc_info.value.detail["message"] == "Bearer token required."


def test_authorize_bearer_roles_rejects_unmapped_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CIVIC_TEST_AUTH_TOKEN_ROLES", '{"reader-token": ["workpaper_reader"]}')

    with pytest.raises(HTTPException) as exc_info:
        authorize_bearer_roles(
            HTTPAuthorizationCredentials(scheme="Bearer", credentials="unknown-token"),
            service_name="CivicBudget",
            feature_name="persisted workpaper retrieval",
            token_roles_env_var="CIVIC_TEST_AUTH_TOKEN_ROLES",
            allowed_roles={"workpaper_reader"},
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail["message"] == "Bearer token not recognized."


def test_authorize_bearer_roles_rejects_token_without_allowed_role(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CIVIC_TEST_AUTH_TOKEN_ROLES", '{"reader-token": ["budget_viewer"]}')

    with pytest.raises(HTTPException) as exc_info:
        authorize_bearer_roles(
            HTTPAuthorizationCredentials(scheme="Bearer", credentials="reader-token"),
            service_name="CivicBudget",
            feature_name="persisted workpaper retrieval",
            token_roles_env_var="CIVIC_TEST_AUTH_TOKEN_ROLES",
            allowed_roles={"workpaper_reader"},
        )

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail["message"] == "Bearer token lacks an allowed role."
    assert exc_info.value.detail["required_roles"] == ["workpaper_reader"]
    assert exc_info.value.detail["token_roles"] == ["budget_viewer"]


def test_authorize_bearer_roles_returns_principal_for_allowed_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "CIVIC_TEST_AUTH_TOKEN_ROLES",
        '{"reader-token": ["workpaper_reader", "budget_admin"]}',
    )

    principal = authorize_bearer_roles(
        HTTPAuthorizationCredentials(scheme="Bearer", credentials="reader-token"),
        service_name="CivicBudget",
        feature_name="persisted workpaper retrieval",
        token_roles_env_var="CIVIC_TEST_AUTH_TOKEN_ROLES",
        allowed_roles={"workpaper_reader"},
    )

    assert isinstance(principal, AuthenticatedPrincipal)
    assert principal.roles == frozenset({"workpaper_reader", "budget_admin"})


def test_resolve_optional_bearer_roles_allows_anonymous_callers_without_config() -> None:
    principal = resolve_optional_bearer_roles(
        None,
        service_name="CivicClerk",
        feature_name="archive search staff access",
        token_roles_env_var="CIVICCLERK_AUTH_TOKEN_ROLES",
        allowed_roles={"archive_reader"},
    )

    assert principal is None


def test_resolve_optional_bearer_roles_returns_principal_for_configured_staff_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "CIVICCLERK_AUTH_TOKEN_ROLES",
        '{"staff-token": ["archive_reader", "clerk_admin"]}',
    )

    principal = resolve_optional_bearer_roles(
        HTTPAuthorizationCredentials(scheme="Bearer", credentials="staff-token"),
        service_name="CivicClerk",
        feature_name="archive search staff access",
        token_roles_env_var="CIVICCLERK_AUTH_TOKEN_ROLES",
        allowed_roles={"archive_reader"},
    )

    assert isinstance(principal, AuthenticatedPrincipal)
    assert principal.roles == frozenset({"archive_reader", "clerk_admin"})


def test_resolve_optional_bearer_roles_rejects_present_token_without_allowed_role(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "CIVICCLERK_AUTH_TOKEN_ROLES",
        '{"staff-token": ["meeting_editor"]}',
    )

    with pytest.raises(HTTPException) as exc_info:
        resolve_optional_bearer_roles(
            HTTPAuthorizationCredentials(scheme="Bearer", credentials="staff-token"),
            service_name="CivicClerk",
            feature_name="archive search staff access",
            token_roles_env_var="CIVICCLERK_AUTH_TOKEN_ROLES",
            allowed_roles={"archive_reader"},
        )

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail["required_roles"] == ["archive_reader"]


def test_parse_header_role_list_normalizes_comma_delimited_roles() -> None:
    parsed = parse_header_role_list(
        " Clerk_Admin, meeting_editor , city_attorney ",
        header_name="X-Civic-Roles",
    )

    assert parsed == frozenset({"clerk_admin", "meeting_editor", "city_attorney"})


def test_authorize_trusted_header_roles_requires_principal_header() -> None:
    with pytest.raises(HTTPException) as exc_info:
        authorize_trusted_header_roles(
            {"X-Civic-Roles": "clerk_admin"},
            service_name="CivicClerk",
            feature_name="staff workflow access",
            principal_header_name="X-Civic-Principal",
            roles_header_name="X-Civic-Roles",
            allowed_roles={"clerk_admin"},
            provider_name="Entra ID proxy",
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail["message"] == "Trusted identity header missing."
    assert "X-Civic-Principal" in exc_info.value.detail["fix"]
    assert "CivicClerk" in exc_info.value.detail["fix"]
    assert "staff workflow access" in exc_info.value.detail["fix"]


def test_authorize_trusted_header_roles_requires_role_header() -> None:
    with pytest.raises(HTTPException) as exc_info:
        authorize_trusted_header_roles(
            {"X-Civic-Principal": "clerk@example.gov"},
            service_name="CivicClerk",
            feature_name="staff workflow access",
            principal_header_name="X-Civic-Principal",
            roles_header_name="X-Civic-Roles",
            allowed_roles={"clerk_admin"},
            provider_name="Entra ID proxy",
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail["message"] == "Trusted role header missing."
    assert "X-Civic-Roles" in exc_info.value.detail["fix"]
    assert "CivicClerk" in exc_info.value.detail["fix"]
    assert "staff workflow access" in exc_info.value.detail["fix"]


def test_authorize_trusted_header_roles_rejects_underprivileged_identity() -> None:
    with pytest.raises(HTTPException) as exc_info:
        authorize_trusted_header_roles(
            {
                "X-Civic-Principal": "clerk@example.gov",
                "X-Civic-Roles": "records_viewer",
            },
            service_name="CivicClerk",
            feature_name="staff workflow access",
            principal_header_name="X-Civic-Principal",
            roles_header_name="X-Civic-Roles",
            allowed_roles={"clerk_admin", "meeting_editor"},
            provider_name="Entra ID proxy",
        )

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail["message"] == "Trusted identity lacks an allowed role."
    assert exc_info.value.detail["principal"] == "clerk@example.gov"
    assert exc_info.value.detail["principal_roles"] == ["records_viewer"]
    assert exc_info.value.detail["required_roles"] == ["clerk_admin", "meeting_editor"]
    assert "CivicClerk" in exc_info.value.detail["fix"]
    assert "staff workflow access" in exc_info.value.detail["fix"]


def test_authorize_trusted_header_roles_returns_principal() -> None:
    principal = authorize_trusted_header_roles(
        {
            "X-Civic-Principal": "clerk@example.gov",
            "X-Civic-Roles": "meeting_editor, clerk_admin",
        },
        service_name="CivicClerk",
        feature_name="staff workflow access",
        principal_header_name="X-Civic-Principal",
        roles_header_name="X-Civic-Roles",
        allowed_roles={"clerk_admin"},
        provider_name="Entra ID proxy",
    )

    assert isinstance(principal, AuthenticatedPrincipal)
    assert principal.auth_method == "trusted_header"
    assert principal.subject == "clerk@example.gov"
    assert principal.provider == "Entra ID proxy"
    assert principal.roles == frozenset({"clerk_admin", "meeting_editor"})
    assert principal.token_fingerprint


def test_resolve_optional_trusted_header_roles_allows_anonymous_callers() -> None:
    principal = resolve_optional_trusted_header_roles(
        {},
        service_name="CivicClerk",
        feature_name="staff workflow access",
        principal_header_name="X-Civic-Principal",
        roles_header_name="X-Civic-Roles",
        allowed_roles={"clerk_admin"},
        provider_name="Entra ID proxy",
    )

    assert principal is None


def test_resolve_optional_trusted_header_roles_returns_principal_when_present() -> None:
    principal = resolve_optional_trusted_header_roles(
        {
            "X-Civic-Principal": "clerk@example.gov",
            "X-Civic-Roles": "clerk_admin",
        },
        service_name="CivicClerk",
        feature_name="staff workflow access",
        principal_header_name="X-Civic-Principal",
        roles_header_name="X-Civic-Roles",
        allowed_roles={"clerk_admin"},
        provider_name="Entra ID proxy",
    )

    assert isinstance(principal, AuthenticatedPrincipal)
    assert principal.subject == "clerk@example.gov"
