# Changelog

All notable changes to **civiccore** are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

CivicCore is the shared platform package for the
[CivicSuite](https://github.com/scottconverse/civicsuite) open-source
municipal operations suite. Per the CivicCore Extraction Spec section 16,
breaking changes to the public API surface (Appendix A of that spec) ship
as MAJOR releases; new symbols or backward-compatible behavior ship as
MINOR; bug fixes ship as PATCH.

## [Unreleased]

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
- Smoke test asserting `import civiccore` succeeds and `__version__`
  begins with `0.1.`.
- Alembic `env.py` stub documenting the migration-ordering contract from
  CivicCore Extraction Spec section 14: CivicCore migrations run first;
  module migrations declare `depends_on` against the CivicCore baseline
  revision; shared-table schema changes are MAJOR releases.
- Apache 2.0 `LICENSE`, `README.md`, `CONTRIBUTING.md` (with the
  bug-routing decision tree from spec section 18), `.gitignore`, and
  placeholder `civiccore-ui/` npm package directory.
- `civiccore.migrations.guards` — three idempotent op wrappers (`idempotent_create_table`, `idempotent_add_column`, `idempotent_alter_column`) plus `has_table` helper.
- `civiccore.migrations.runner` — `upgrade_to_head(connection)` and `current_revision(connection)` entry points for consuming modules' env.py.
- `civiccore/migrations/alembic.ini` + `civiccore/migrations/env.py` — civiccore's own Alembic wiring (`alembic_version_civiccore` version table to avoid collision with consuming modules).
- `civiccore_0001_baseline_v1` migration — idempotent snapshot of the 16 civiccore-owned shared tables at records HEAD `019_encrypt_connection_config`, per ADR-0003.
- `tests/test_baseline_idempotency.py` — pytest asserting the baseline runs clean on an empty DB and is a no-op against an already-populated DB.

### Changed
- License switched from MIT to Apache License 2.0 to match civicrecords-ai
  (which is Apache-2.0). Spec doc 02 Appendix D and CONSISTENCY.md
  section 6 are being updated in the umbrella repo in the same change.
- `docs/index.html` landing page added to satisfy the project's pre-push
  documentation gate.

No release sections yet — `0.1.0` ships with Phase 1 of the CivicCore
extraction (shared models + audit chain), per spec section 12.
