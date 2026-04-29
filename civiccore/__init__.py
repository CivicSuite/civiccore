"""CivicCore shared platform package for the CivicSuite municipal suite.

Current development-line surface includes migrations, a shared SQLAlchemy
``Base``, LLM helpers, hash-chained audit primitives, source/provenance
metadata contracts, offline import/export manifests, export bundle helpers,
local city profile configuration, and bearer-token auth helpers for
protected or mixed public/staff FastAPI routes. CivicCore is a library,
not an end-user application.
"""

from __future__ import annotations

__version__ = "0.6.0"

from civiccore.audit import AuditActor, AuditEvent, AuditHashChain, AuditSubject
from civiccore.city_profile import (
    CityProfile,
    DepartmentProfile,
    DeploymentProfile,
    ModuleEnablement,
    load_city_profile,
)
from civiccore.connectors import (
    ExportManifest,
    ImportManifest,
    ManifestFile,
    ManifestValidationError,
    validate_manifest,
)
from civiccore.exports import (
    BundleFile,
    ExportBundle,
    build_sha256sums,
    validate_bundle,
    write_manifest,
)
from civiccore.provenance import (
    CitationTarget,
    DocumentMetadata,
    ProvenanceBundle,
    SourceKind,
    SourceReference,
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
    "normalized_text_sha256",
    "validate_release_browser_evidence",
]
