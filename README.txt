CivicCore
=========

Shared platform library for the CivicSuite open-source municipal operations
suite. https://github.com/CivicSuite/civicsuite

What this is
------------

CivicCore is the Python library every CivicSuite module depends on for shared
platform plumbing. It is not an end-user municipal app.

What ships in the current development line:

  - civiccore.migrations - migration runner with idempotent guards plus the
    civiccore_0001_baseline_v1 shared-schema baseline and civiccore_0002_llm.
  - civiccore.db - shared SQLAlchemy declarative Base.
  - civiccore.llm - providers, prompt templates, model registry, context
    utilities, and structured output.
  - civiccore.audit - hash-chained audit primitives.
  - civiccore.provenance - source/provenance metadata contracts.
  - civiccore.connectors - offline import/export manifest schemas plus
    local-first import helpers for supported agenda-platform payloads.
  - civiccore.exports - static export-bundle manifest and checksum helpers.
  - civiccore.city_profile - local city/deployment configuration models.
  - civiccore.auth - bearer-token role helpers for protected or mixed
    public/staff FastAPI routes.
  - civiccore.verification - content-bound browser release-evidence helpers.
  - civiccore.search - deterministic text normalization, matching, and
    reciprocal-rank-fusion helpers.
  - civiccore.notifications - notice deadline planning and publication
    compliance helpers with actionable warning codes.

Still planned extraction targets:

  civiccore.catalog, civiccore.exemptions, civiccore.ingest,
  civiccore.scaffold.
  civiccore.onboarding now ships storage-neutral profile interview
  helpers, but not a web onboarding UI or persistence router.

Live connector sync, credential storage, vendor write-back, document ingestion,
search indexing, notification delivery queues, and legal determinations are
still not shipped platform behaviors.

Status
------

v0.11.0 is the latest published release. The current line now includes shared onboarding profile helpers on top of auth
helpers, verification helpers, shared search helpers, local-first connector
import helpers, and notice deadline/compliance helpers on top of the audit,
provenance, manifest, export-bundle, city-profile, migration, and LLM
primitives. v0.2.0 shipped the
civiccore.llm module. v0.1.0 shipped the migration baseline.

Install
-------

From the current published GitHub release wheel:

    pip install https://github.com/CivicSuite/civiccore/releases/download/v0.9.0/civiccore-0.9.0-py3-none-any.whl

CivicCore is distributed as versioned GitHub release artifacts (not on PyPI).
Each release publishes SHA256SUMS.txt alongside the wheel and sdist. Verify
checksums before promoting an artifact downstream.

For development from a clone:

    git clone https://github.com/CivicSuite/civiccore.git
    cd civiccore
    pip install -e .[dev]

Public API surface (high level)
-------------------------------

  civiccore.llm
    LLMProvider, register_provider, get_provider, list_providers
    OllamaProvider, OpenAIProvider, AnthropicProvider, build_provider
    PromptTemplate, RenderedPrompt, render_template, resolve_template
    ModelRegistry, model_registry_router, get_active_model
    TokenBudget, ContextBlock, assemble_context, blocks_to_prompt
    sanitize_for_llm, StructuredOutput, StructuredOutputFailure

  civiccore.audit
    AuditActor, AuditSubject, AuditEvent, AuditHashChain

  civiccore.provenance
    SourceKind, SourceReference, CitationTarget, DocumentMetadata,
    ProvenanceBundle

  civiccore.connectors / civiccore.exports
    ConnectorImportError, ImportedAgendaItem, ImportedMeeting,
    SUPPORTED_CONNECTORS, import_meeting_payload,
    ImportManifest, ExportManifest, ManifestFile, validate_manifest,
    ExportBundle, BundleFile, write_manifest, build_sha256sums,
    validate_bundle

  civiccore.city_profile
    CityProfile, DepartmentProfile, DeploymentProfile, ModuleEnablement,
    load_city_profile

  civiccore.onboarding
    OnboardingField, OnboardingProgress, DEFAULT_PROFILE_FIELDS,
    parse_profile_answer, compute_onboarding_status,
    completed_profile_fields, next_profile_prompt

  civiccore.migrations / civiccore.db
    Migration runner, civiccore_0001_baseline_v1 shared schema, and Base

Compatibility
-------------

Current v0.1.0 module foundations still pin older civiccore lines.
Production-depth consumers can move to civiccore ==0.11.0 now that the release is published and the suite
compatibility matrix are updated.

The suite-wide compatibility matrix is maintained at:
https://github.com/CivicSuite/civicsuite/tree/main/docs/compatibility

License
-------

Apache License 2.0. See LICENSE.

Contributing
------------

See CONTRIBUTING.md, including the decision tree for where to file a bug
across the CivicSuite multi-repo layout.

Source
------

https://github.com/CivicSuite/civiccore
