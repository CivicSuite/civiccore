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
- `civiccore_0002_llm` migration: evolves `prompt_templates` for Phase 2 override-resolution columns (`template_name` rename, `consumer_app`, `is_override`); adds `idempotent_drop_constraint` guard helper
- `civiccore.llm.registry`: `ModelRegistry` ORM + Pydantic schemas (`ModelRegistryCreate`, `ModelRegistryRead`, `ModelRegistryUpdate`)
- `civiccore.llm.templates`: `PromptTemplate` ORM + Pydantic schemas (`PromptTemplateCreate`, `PromptTemplateRead`, `PromptTemplateUpdate`)
- `civiccore.db.Base`: shared SQLAlchemy declarative base for civiccore ORM models
- `civiccore.llm.providers`: pluggable provider abstraction.
  - `LLMProvider` ABC with `generate`, `embed`, `embed_batch`, `name`, `supports_images` (per ADR-0004 §6).
  - Decorator-based registry: `@register_provider`, `get_provider`, `list_providers`.
  - Built-in providers: `OllamaProvider` (uses httpx, default model `gemma4:e4b`), `OpenAIProvider` (optional extra `civiccore[openai]`), `AnthropicProvider` (optional extra `civiccore[anthropic]`; embeddings raise `NotImplementedError` since Anthropic has no native embed endpoint).
  - Optional cloud SDKs: install `openai` or `anthropic` directly (e.g. `pip install openai`); the `civiccore[openai]` and `civiccore[anthropic]` extras shorthand becomes available once civiccore is published to PyPI.

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
