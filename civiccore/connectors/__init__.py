"""CivicCore: connector framework (Connector ABC, registry, encrypted credentials). Module-agnostic adapters only; module-specific connectors stay module-side. Phase 3 extraction target."""

from civiccore.connectors.manifest import (
    ExportManifest,
    ImportManifest,
    ManifestFile,
    ManifestValidationError,
    validate_manifest,
)

__all__ = [
    "ExportManifest",
    "ImportManifest",
    "ManifestFile",
    "ManifestValidationError",
    "validate_manifest",
]
