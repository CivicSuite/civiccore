"""Shared offline connector primitives for current CivicSuite consumers."""

from civiccore.connectors.imports import (
    ConnectorImportError,
    ImportedAgendaItem,
    ImportedMeeting,
    SUPPORTED_CONNECTORS,
    import_meeting_payload,
)
from civiccore.connectors.manifest import (
    ExportManifest,
    ImportManifest,
    ManifestFile,
    ManifestValidationError,
    validate_manifest,
)
from civiccore.connectors.sync import (
    SyncCircuitPolicy,
    SyncCircuitState,
    SyncHealthStatus,
    SyncOperatorStatus,
    SyncRetryExhausted,
    SyncRetryPolicy,
    SyncRunResult,
    apply_sync_run_result,
    build_sync_operator_status,
    compute_retry_delay,
    compute_sync_health_status,
    with_http_retry,
)

__all__ = [
    "ConnectorImportError",
    "ExportManifest",
    "ImportedAgendaItem",
    "ImportedMeeting",
    "ImportManifest",
    "ManifestFile",
    "ManifestValidationError",
    "SUPPORTED_CONNECTORS",
    "SyncCircuitPolicy",
    "SyncCircuitState",
    "SyncHealthStatus",
    "SyncOperatorStatus",
    "SyncRetryExhausted",
    "SyncRetryPolicy",
    "SyncRunResult",
    "apply_sync_run_result",
    "build_sync_operator_status",
    "compute_retry_delay",
    "compute_sync_health_status",
    "import_meeting_payload",
    "validate_manifest",
    "with_http_retry",
]
