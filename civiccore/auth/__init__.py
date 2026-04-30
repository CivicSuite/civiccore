"""Authentication helpers for CivicSuite FastAPI services."""

from civiccore.auth.bearer import (
    AuthenticatedPrincipal,
    authorize_bearer_roles,
    parse_token_role_map,
    resolve_optional_bearer_roles,
)
from civiccore.auth.trusted_headers import (
    authorize_trusted_header_roles,
    parse_header_role_list,
    resolve_optional_trusted_header_roles,
)

__all__ = [
    "AuthenticatedPrincipal",
    "authorize_bearer_roles",
    "authorize_trusted_header_roles",
    "parse_header_role_list",
    "parse_token_role_map",
    "resolve_optional_bearer_roles",
    "resolve_optional_trusted_header_roles",
]
