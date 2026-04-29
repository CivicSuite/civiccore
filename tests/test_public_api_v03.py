"""Smoke tests for the shipped CivicCore package-root surface."""

from __future__ import annotations


def test_v03_public_api_symbols_import_from_package_root() -> None:
    import civiccore

    expected = {
        "AuditActor",
        "AuditEvent",
        "AuditHashChain",
        "AuditSubject",
        "SourceKind",
        "SourceReference",
        "CitationTarget",
        "DocumentMetadata",
        "ProvenanceBundle",
        "ConnectorImportError",
        "ImportManifest",
        "ExportManifest",
        "ImportedAgendaItem",
        "ImportedMeeting",
        "ManifestFile",
        "ManifestValidationError",
        "SUPPORTED_CONNECTORS",
        "import_meeting_payload",
        "validate_manifest",
        "BundleFile",
        "ExportBundle",
        "build_sha256sums",
        "validate_bundle",
        "write_manifest",
        "CityProfile",
        "DepartmentProfile",
        "DeploymentProfile",
        "ModuleEnablement",
        "load_city_profile",
        "normalize_search_query",
        "normalize_search_text",
        "search_text_matches_query",
        "reciprocal_rank_fusion",
        "normalized_text_sha256",
        "validate_release_browser_evidence",
    }

    missing = expected - set(dir(civiccore))
    assert not missing, f"Missing shipped public symbols: {missing}"


def test_v03_placeholder_modules_stay_out_of_root_surface() -> None:
    import civiccore

    not_yet_shipped = {
        "Auth",
        "NotificationDelivery",
        "ExemptionRuleEngine",
        "DocumentIngestor",
    }

    assert not (not_yet_shipped & set(dir(civiccore)))
