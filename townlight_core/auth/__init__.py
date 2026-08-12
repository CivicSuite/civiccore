"""Authentication helpers for Townlight FastAPI services."""

from townlight_core.auth.bearer import (
    AuthenticatedPrincipal,
    authorize_bearer_roles,
    parse_token_role_map,
    resolve_optional_bearer_roles,
)
from townlight_core.auth.staff_key import staff_key_gate
from townlight_core.auth.suite_session import (
    SuiteSessionConfigError,
    SuiteSessionPrincipal,
    issue_suite_session_token,
    revoke_suite_session,
    validate_suite_session_token,
)
from townlight_core.auth.trusted_headers import (
    authorize_trusted_header_roles,
    enforce_trusted_proxy_source,
    load_trusted_header_auth_config,
    parse_header_role_list,
    resolve_optional_trusted_header_roles,
    TrustedHeaderAuthConfig,
)

__all__ = [
    "AuthenticatedPrincipal",
    "SuiteSessionConfigError",
    "SuiteSessionPrincipal",
    "authorize_bearer_roles",
    "authorize_trusted_header_roles",
    "enforce_trusted_proxy_source",
    "issue_suite_session_token",
    "load_trusted_header_auth_config",
    "parse_header_role_list",
    "parse_token_role_map",
    "resolve_optional_bearer_roles",
    "resolve_optional_trusted_header_roles",
    "revoke_suite_session",
    "staff_key_gate",
    "TrustedHeaderAuthConfig",
    "validate_suite_session_token",
]
