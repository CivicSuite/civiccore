"""Authentication helpers for CivicSuite FastAPI services."""

from civiccore.auth.bearer import (
    AuthenticatedPrincipal,
    authorize_bearer_roles,
    parse_token_role_map,
    resolve_optional_bearer_roles,
)

__all__ = [
    "AuthenticatedPrincipal",
    "authorize_bearer_roles",
    "parse_token_role_map",
    "resolve_optional_bearer_roles",
]
