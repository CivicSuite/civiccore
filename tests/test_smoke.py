"""Smoke test - proves the package is importable and version-tagged."""


def test_import_civiccore() -> None:
    import civiccore

    assert civiccore.__version__ == "0.20.0"
    assert civiccore.roles_grant_access
    assert civiccore.access_level_allows
    assert civiccore.filter_records_by_access_level
    assert civiccore.AuditHashChain
    assert civiccore.PersistedAuditLogEntry
    assert callable(civiccore.compute_persisted_audit_hash)
    assert callable(civiccore.verify_persisted_audit_chain)
    assert civiccore.SourceReference
    assert civiccore.ExportManifest
    assert civiccore.ExportBundle
    assert civiccore.CityProfile
    assert civiccore.reciprocal_rank_fusion
    assert civiccore.import_meeting_payload
    assert civiccore.DiscoveredRecord
    assert civiccore.FetchedDocument
    assert civiccore.SourceMaterial
    assert civiccore.validate_cited_sentences
    assert civiccore.build_deadline_plan
    assert civiccore.evaluate_notice_compliance
    assert civiccore.encrypt_json
    assert civiccore.validate_url_host
    assert civiccore.normalize_trusted_proxy_cidrs
    assert civiccore.is_trusted_proxy_ip
