# Changelog

All notable changes to **civiccore** are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

CivicCore is the shared platform package for the
[CivicSuite](https://github.com/CivicSuite/civicsuite) open-source
municipal operations suite. Per the CivicCore Extraction Spec section 16,
breaking changes to the public API surface (Appendix A of that spec) ship
as MAJOR releases; new symbols or backward-compatible behavior ship as
MINOR; bug fixes ship as PATCH.

## [Unreleased]

### Added
- `civiccore.search.normalize_search_text()` and
  `normalize_search_query()` now ship a deterministic shared
  normalization surface for current CivicSuite consumers that need
  case-insensitive, whitespace-stable text matching without pulling in a
  database or embedding runtime.
- `civiccore.search.search_text_matches_query()` now ships a tiny shared
  substring-matching helper so mixed public/staff consumer routes can
  reuse one query-normalization contract instead of reimplementing it
  per module.
- `civiccore.search.reciprocal_rank_fusion()` now ships a generic hybrid
  ranking helper for consumers that need to merge semantic and lexical
  search results without extracting a full search engine.
- `civiccore.verification.validate_release_browser_evidence()` validates
  content-bound browser QA release manifests so downstream modules can
  prove that desktop/mobile screenshots still match the current rendered
  page source across Windows and Linux checkouts.
- `civiccore.verification.normalized_text_sha256()` hashes UTF-8 text
  with normalized newlines so cross-platform browser QA evidence does
  not fail purely because of line-ending differences.

### Changed
- README and placeholder docs now describe `civiccore.search` as a
  partially shipped helper namespace instead of a future-only placeholder
  package.
- README and verification placeholder docs now describe
  `civiccore.verification` as a partially shipped helper namespace
  instead of a reserved future-only package.
- Package metadata and release verification now target the upcoming
  `0.7.0` minor line so the first shipped shared search helpers do not
  retroactively change the published `0.6.0` contract.

## [0.6.0] - 2026-04-29

### Added
- `civiccore.verification.validate_release_browser_evidence()` validates
  content-bound browser QA release manifests so downstream modules can
  prove that desktop/mobile screenshots still match the current rendered
  page source across Windows and Linux checkouts.
- `civiccore.verification.normalized_text_sha256()` hashes UTF-8 text
  with normalized newlines so cross-platform browser QA evidence does
  not fail purely because of line-ending differences.

### Changed
- README and verification placeholder docs now describe
  `civiccore.verification` as a partially shipped helper namespace
  instead of a reserved future-only package.
- Package metadata and release verification now target the upcoming
  `0.6.0` minor line so the first shipped verification helper does not
  retroactively change the published `0.5.0` contract.

## [0.5.0] - 2026-04-29

### Added
- `civiccore.auth` now ships a minimal bearer-token role helper for
  downstream FastAPI services that need actionable `401`/`403`/`503`
  protection on non-public internal routes without introducing a full
  identity-provider stack.
- `civiccore.auth.resolve_optional_bearer_roles()` now supports mixed
  public/staff endpoints that should keep anonymous access available
  while upgrading privileged results to the shared bearer-token role
  contract when callers present Authorization headers.

### Changed
- README and auth placeholder docs now describe `civiccore.auth` as a
  shipped helper namespace instead of a reserved future-only package.
- Package metadata and release verification now target the upcoming
  `0.5.0` minor line so the optional mixed-route auth helper does not
  retroactively change the published `0.4.0` contract.

## [0.3.0] - 2026-04-28

This release adds the shared offline primitives needed for CivicSuite's first
production-depth municipal workflows. It is backward-compatible with v0.2.0
and does not introduce auth/RBAC, live connector sync, document ingestion,
search indexing, notification delivery, or vendor write-back.

### Added
- `civiccore.audit`: storage-neutral hash-chained audit primitives
  (`AuditActor`, `AuditSubject`, `AuditEvent`, `AuditHashChain`) for downstream
  modules that need tamper-evident local audit trails.
- `civiccore.provenance`: source/provenance metadata contracts
  (`SourceKind`, `SourceReference`, `CitationTarget`, `DocumentMetadata`,
  `ProvenanceBundle`) for citations, source manifests, and export metadata.
- `civiccore.connectors`: offline import/export manifest schemas
  (`ImportManifest`, `ExportManifest`, `ManifestFile`, `validate_manifest`)
  with path, size, and SHA-256 validation.
- `civiccore.exports`: static export-bundle helpers (`ExportBundle`,
  `BundleFile`, `write_manifest`, `build_sha256sums`, `validate_bundle`) for
  reproducible offline bundles.
- `civiccore.city_profile`: local city/deployment configuration models
  (`CityProfile`, `DepartmentProfile`, `DeploymentProfile`,
  `ModuleEnablement`, `load_city_profile`) with JSON support and optional YAML
  loading when PyYAML is installed.
- Package-root exports for the v0.3.0 primitives, plus public API smoke tests
  proving shipped symbols are exposed and planned symbols are not accidentally
  promoted.

## [0.2.0] - 2026-04-25

This release ships the `civiccore.llm` module — provider abstraction
(Ollama / OpenAI / Anthropic), prompt template engine with a 3-step
override resolver, model registry service + admin router, context
utilities with prompt-injection defense, structured-output helper, and the
full public `civiccore.llm` import surface.

### Added
- `civiccore_0002_llm` migration: evolves `prompt_templates` for Phase 2 override-resolution columns (`template_name` rename, `consumer_app`, `is_override`); adds `idempotent_drop_constraint` guard helper
- `civiccore.llm.registry`: `ModelRegistry` ORM + Pydantic schemas (`ModelRegistryCreate`, `ModelRegistryRead`, `ModelRegistryUpdate`)
- `civiccore.llm.templates`: `PromptTemplate` ORM + Pydantic schemas (`PromptTemplateCreate`, `PromptTemplateRead`, `PromptTemplateUpdate`)
- `civiccore.db.Base`: shared SQLAlchemy declarative base for civiccore ORM models
- `civiccore.llm.providers`: pluggable provider abstraction.
  - `LLMProvider` ABC with `generate`, `embed`, `embed_batch`, `name`, `supports_images` (per ADR-0004 §6).
  - Decorator-based registry: `@register_provider`, `get_provider`, `list_providers`.
  - Built-in providers: `OllamaProvider` (uses httpx, default model `gemma4:e4b`), `OpenAIProvider` (optional extra `civiccore[openai]`), `AnthropicProvider` (optional extra `civiccore[anthropic]`; embeddings raise `NotImplementedError` since Anthropic has no native embed endpoint).
  - Optional cloud SDKs: install `openai` or `anthropic` directly (e.g. `pip install openai`); the `civiccore[openai]` and `civiccore[anthropic]` extras shorthand becomes available once civiccore is published to PyPI.
- `civiccore.llm.templates`: rendering and override resolution (Step 3c).
  - `render_template(template, variables)` returns a `RenderedPrompt` dataclass with `system` / `user` / `template_name` / `consumer_app` / `version`.
  - `resolve_template(session, *, template_name, consumer_app)` async helper implements the 3-step resolution per ADR-0004 §7: app DB override (consumer_app + is_override=true + is_active + highest version) → app code-level override (`OVERRIDE_REGISTRY`) → civiccore default (consumer_app='civiccore' + is_override=false + is_active + highest version) → `PromptTemplateNotFoundError`.
  - New exceptions: `PromptTemplateError` (base), `PromptTemplateNotFoundError`, `PromptTemplateRenderError` (names the missing variable).
  - Uses stdlib `string.Template` per ADR-0004 (no Jinja2; `$name` syntax avoids JSON-brace collisions).
- `civiccore.llm` (Step 3d): finalized public API surface for downstream consumption.
  - Context utilities ported from records-ai: `TokenBudget`, `ContextBlock`, `estimate_tokens`, `count_tokens`, `sanitize_for_llm` (3-pattern prompt-injection defense), `assemble_context`, `blocks_to_prompt`, `DEFAULT_CONTEXT_WINDOW=8192`.
  - `civiccore.llm.structured`: `StructuredOutput[ModelT]` Pydantic-validated LLM-call helper with retry-on-malformed (default 3 attempts); `StructuredOutputFailure` exception. Provider-agnostic.
  - `civiccore.llm.registry.service`: async `get_active_model`, `require_active_model` (raises `MissingModelError`), `get_active_model_context_window` (defaults to 8192). Library-friendly: takes `AsyncSession` parameter, no hardcoded session_maker.
  - `civiccore.llm.registry.router`: FastAPI APIRouter for ModelRegistry admin CRUD (list / get / post / patch / delete). Mountable; consumers override `get_session` dependency.
  - Single import surface: `from civiccore.llm import ...` exposes the full public API for records-ai Step 5 consumption.
- Per ADR-0004 §3: NO cost tracking, NO spend logging, NO `llm_call_log` table introduced. Token budgeting is context-window math only.
- **Audit fix (RESOLVER-001):** template resolver upgraded from 2-step to 3-step per ADR-0004 §7. Added `civiccore.llm.templates.overrides` module with `OVERRIDE_REGISTRY`, `register_template_override`, and `unregister_template_override`. Resolution order is now: app DB override → app code-level override → civiccore DB default → `PromptTemplateNotFoundError`. DB overrides win over code overrides (operators retain production hot-fix capability).
- **Audit fix (PROVIDER-CONFIG-001):** added Pydantic config schemas (`OllamaConfig`, `OpenAIConfig`, `AnthropicConfig`) and `civiccore.llm.factory.build_provider(name, config)` per ADR-0004 §6. Validates config type matches the registered provider before construction. Direct provider constructor calls remain supported for backwards compatibility.

## [0.1.0] - 2026-04-24

### Added
- Initial package skeleton with empty subpackages for the 14 subsystems
  specified in CivicCore Extraction Spec Appendix B: `auth`, `audit`,
  `llm`, `ingest`, `search`, `connectors`, `notifications`, `onboarding`,
  `catalog`, `exemptions`, `verification`, `models`, `migrations`, and
  `scaffold`.
- `pyproject.toml` with shared dependency pins matching
  civicrecords-ai/backend/pyproject.toml (FastAPI, SQLAlchemy, Alembic,
  fastapi-users, pgvector, redis, celery, pydantic, uvicorn, ollama-stack
  ingest libs, etc.). Python `>=3.11` to support modules that have not yet
  moved to 3.12.
- Smoke test asserting `import civiccore` succeeds and the package exports
  the release version.
- Apache 2.0 `LICENSE`, `README.md`, `CONTRIBUTING.md`, `.gitignore`, and
  placeholder `civiccore-ui/` npm package directory.
- `civiccore.migrations.guards` — idempotent wrappers for table, column,
  index, foreign-key, unique-constraint, and check-constraint creation,
  plus `has_table`.
- `civiccore.migrations.runner` — `upgrade_to_head()` and
  `current_revision(connection)` entry points for consuming modules'
  Alembic env.py wiring.
- `civiccore/migrations/alembic.ini` + `civiccore/migrations/env.py` —
  civiccore's own Alembic wiring (`alembic_version_civiccore` version table
  to avoid collision with consuming modules).
- `civiccore_0001_baseline_v1` migration — idempotent snapshot of the 16
  civiccore-owned shared tables at CivicRecords AI HEAD
  `019_encrypt_connection_config`, per ADR-0003.
- `tests/test_baseline_idempotency.py` — pytest asserting the baseline runs
  clean on an empty DB and is a no-op against an already-populated DB.
- `.github/workflows/ci.yml` — CI workflow on `pull_request`/`push` to
  `main` running smoke + baseline idempotency tests.
- `.github/workflows/release.yml` — tag-driven build that publishes a
  versioned wheel and source distribution to GitHub Releases so downstream
  apps can depend on a release artifact instead of a Git SHA pin.

### Changed
- License switched from MIT to Apache License 2.0 to match
  civicrecords-ai.
- `docs/index.html` landing page added to satisfy the project's pre-push
  documentation gate.
- README, CONTRIBUTING, pyproject.toml, and CHANGELOG: stale
  `scottconverse/civiccore` and `scottconverse/civicsuite` URLs corrected
  to `CivicSuite/civiccore` and `CivicSuite/civicsuite`.
- Hardened the tag-driven release workflow so it runs
  `scripts/verify-release.sh` before publishing GitHub release artifacts.
- Release artifacts now include `SHA256SUMS.txt` so downstream modules can
  verify the wheel and source distribution they consume.
- `scripts/verify-release.sh` now creates a clean virtualenv, installs the
  freshly built wheel, asserts the exact package version, and smoke-imports the
  migration runner before a release can pass.
- `tests/test_smoke.py` now asserts the exact `0.1.0` release version instead
  of accepting any `0.1.x` prefix.
