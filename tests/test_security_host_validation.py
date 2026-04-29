from __future__ import annotations

import pytest

from civiccore.security import (
    BLOCK_REASON,
    extract_odbc_host,
    is_blocked_host,
    normalize_allowlist,
    validate_odbc_connection_string,
    validate_url_host,
)


def test_normalize_allowlist_is_case_insensitive_and_trims_whitespace() -> None:
    assert normalize_allowlist([" Example.Gov ", "", "10.0.0.5"]) == {
        "example.gov",
        "10.0.0.5",
    }


@pytest.mark.parametrize("host", ["localhost", "127.0.0.1", "10.0.0.8", "192.168.1.20", "::1", ""])
def test_is_blocked_host_rejects_local_and_private_targets(host: str) -> None:
    assert is_blocked_host(host) is True


def test_is_blocked_host_honors_exact_allowlist() -> None:
    assert is_blocked_host("localhost", ["LOCALHOST"]) is False
    assert is_blocked_host("10.0.0.8", ["10.0.0.8"]) is False


def test_validate_url_host_raises_actionable_error_for_blocked_targets() -> None:
    with pytest.raises(ValueError, match="Connector URL 'http://localhost/api':"):
        validate_url_host("http://localhost/api")


def test_validate_url_host_allows_named_hosts_and_explicit_allowlist() -> None:
    validate_url_host("https://records.vendor.example/api")
    validate_url_host("http://10.0.0.8/api", ["10.0.0.8"])


def test_extract_odbc_host_handles_braced_values_and_ports() -> None:
    assert extract_odbc_host("Driver={ODBC Driver 18};Server={sql.internal,1433};Database=foo") == (
        "sql.internal"
    )


def test_validate_odbc_connection_string_fails_closed_when_host_missing() -> None:
    with pytest.raises(ValueError, match="does not contain a parseable Server/Host/Data Source"):
        validate_odbc_connection_string("Driver={ODBC Driver 18};Database=foo")


def test_validate_odbc_connection_string_blocks_private_hosts_with_fix_path() -> None:
    with pytest.raises(ValueError, match="blocked range"):
        validate_odbc_connection_string("Driver={ODBC Driver 18};Server=192.168.1.9;Database=foo")


def test_block_reason_mentions_allowlist_fix_path() -> None:
    assert "allowlist" in BLOCK_REASON
