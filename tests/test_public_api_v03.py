"""Smoke tests for the shipped CivicCore package-root surface."""

from __future__ import annotations


def test_v03_public_api_symbols_import_from_package_root() -> None:
    import civiccore

    expected = {
        "AuditActor",
        "AuditEvent",
        "AuditHashChain",
        "AuditSubject",
        "PersistedAuditLogEntry",
        "ZERO_HASH",
        "canonical_audit_actor_id",
        "canonical_audit_details",
        "canonical_audit_timestamp",
        "compute_persisted_audit_hash",
        "verify_persisted_audit_chain",
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
        "CitedSentence",
        "CitationValidationError",
        "DiscoveredRecord",
        "DeadlinePlan",
        "NoticeComplianceResult",
        "NoticeComplianceWarning",
        "SPECIAL_NOTICE_TYPES",
        "build_deadline_plan",
        "evaluate_notice_compliance",
        "CityProfile",
        "DepartmentProfile",
        "DeploymentProfile",
        "ModuleEnablement",
        "load_city_profile",
        "FetchedDocument",
        "HealthCheckResult",
        "HealthStatus",
        "OnboardingField",
        "OnboardingProgress",
        "DEFAULT_PROFILE_FIELDS",
        "completed_profile_fields",
        "compute_onboarding_status",
        "encrypt_json",
        "decrypt_json",
        "is_encrypted",
        "is_trusted_proxy_ip",
        "normalize_trusted_proxy_cidrs",
        "validate_url_host",
        "validate_odbc_connection_string",
        "next_profile_prompt",
        "parse_profile_answer",
        "SourceMaterial",
        "normalize_search_query",
        "normalize_search_text",
        "search_text_matches_query",
        "reciprocal_rank_fusion",
        "validate_cited_sentences",
        "normalized_text_sha256",
        "validate_release_browser_evidence",
    }

    missing = expected - set(dir(civiccore))
    assert not missing, f"Missing shipped public symbols: {missing}"


def test_v03_placeholder_modules_stay_out_of_root_surface() -> None:
    import civiccore

    not_yet_shipped = {
        "Auth",
        "ExemptionRuleEngine",
    }

    assert not (not_yet_shipped & set(dir(civiccore)))
