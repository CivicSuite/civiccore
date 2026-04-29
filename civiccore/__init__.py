"""CivicCore shared platform package for the CivicSuite municipal suite.

Current development-line surface includes migrations, a shared SQLAlchemy
``Base``, LLM helpers, hash-chained audit primitives, source/provenance
metadata contracts, offline import/export manifests, export bundle helpers,
local city profile configuration, and bearer-token auth helpers for
protected or mixed public/staff FastAPI routes. CivicCore is a library,
not an end-user application.
"""

from __future__ import annotations

__version__ = "0.13.0"

from civiccore.audit import AuditActor, AuditEvent, AuditHashChain, AuditSubject
from civiccore.city_profile import (
    CityProfile,
    DepartmentProfile,
    DeploymentProfile,
    ModuleEnablement,
    load_city_profile,
)
from civiccore.connectors import (
    ConnectorImportError,
    ExportManifest,
    ImportedAgendaItem,
    ImportedMeeting,
    ImportManifest,
    ManifestFile,
    ManifestValidationError,
    SUPPORTED_CONNECTORS,
    import_meeting_payload,
    validate_manifest,
)
from civiccore.exports import (
    BundleFile,
    ExportBundle,
    build_sha256sums,
    validate_bundle,
    write_manifest,
)
from civiccore.ingest import (
    CitedSentence,
    CitationValidationError,
    DiscoveredRecord,
    FetchedDocument,
    HealthCheckResult,
    HealthStatus,
    SourceMaterial,
    validate_cited_sentences,
)
from civiccore.notifications import (
    DeadlinePlan,
    NoticeComplianceResult,
    NoticeComplianceWarning,
    SPECIAL_NOTICE_TYPES,
    build_deadline_plan,
    evaluate_notice_compliance,
)
from civiccore.onboarding import (
    DEFAULT_PROFILE_FIELDS,
    OnboardingField,
    OnboardingProgress,
    completed_profile_fields,
    compute_onboarding_status,
    next_profile_prompt,
    parse_profile_answer,
)
from civiccore.provenance import (
    CitationTarget,
    DocumentMetadata,
    ProvenanceBundle,
    SourceKind,
    SourceReference,
)
from civiccore.security import (
    AtRestDecryptionError,
    build_fernet,
    decrypt_json,
    encrypt_json,
    extract_odbc_host,
    is_blocked_host,
    is_encrypted,
    normalize_allowlist,
    validate_odbc_connection_string,
    validate_url_host,
)
from civiccore.search import (
    access_level_allows,
    filter_records_by_access_level,
    normalize_access_value,
    normalize_access_values,
    normalize_search_query,
    normalize_search_text,
    reciprocal_rank_fusion,
    roles_grant_access,
    search_text_matches_query,
)
from civiccore.verification import normalized_text_sha256, validate_release_browser_evidence

__all__ = [
    "__version__",
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
    "CitedSentence",
    "CitationValidationError",
    "DiscoveredRecord",
    "DeadlinePlan",
    "NoticeComplianceResult",
    "NoticeComplianceWarning",
    "SPECIAL_NOTICE_TYPES",
    "build_deadline_plan",
    "evaluate_notice_compliance",
    "DEFAULT_PROFILE_FIELDS",
    "CityProfile",
    "DepartmentProfile",
    "DeploymentProfile",
    "FetchedDocument",
    "HealthCheckResult",
    "HealthStatus",
    "ModuleEnablement",
    "OnboardingField",
    "OnboardingProgress",
    "access_level_allows",
    "completed_profile_fields",
    "compute_onboarding_status",
    "decrypt_json",
    "filter_records_by_access_level",
    "encrypt_json",
    "extract_odbc_host",
    "AtRestDecryptionError",
    "build_fernet",
    "is_blocked_host",
    "is_encrypted",
    "load_city_profile",
    "normalize_access_value",
    "normalize_access_values",
    "normalize_allowlist",
    "next_profile_prompt",
    "normalize_search_query",
    "normalize_search_text",
    "parse_profile_answer",
    "roles_grant_access",
    "search_text_matches_query",
    "reciprocal_rank_fusion",
    "SourceMaterial",
    "validate_cited_sentences",
    "validate_odbc_connection_string",
    "normalized_text_sha256",
    "validate_url_host",
    "validate_release_browser_evidence",
]
