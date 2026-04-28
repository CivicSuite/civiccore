"""Smoke tests for the CivicCore v0.3.0 public primitive surface."""

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
        "ImportManifest",
        "ExportManifest",
        "ManifestFile",
        "ManifestValidationError",
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
    }

    missing = expected - set(dir(civiccore))
    assert not missing, f"Missing v0.3.0 public symbols: {missing}"


def test_v03_placeholder_modules_stay_out_of_root_surface() -> None:
    import civiccore

    not_yet_shipped = {
        "Auth",
        "SearchIndex",
        "NotificationDelivery",
        "ExemptionRuleEngine",
        "DocumentIngestor",
    }

    assert not (not_yet_shipped & set(dir(civiccore)))
