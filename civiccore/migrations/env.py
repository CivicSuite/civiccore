"""Alembic environment for CivicCore shared-table migrations.

STUB ONLY — Phase 0 scaffold. No real migration revisions are seeded yet.
Phase 1 will baseline this against the latest CivicRecords AI migration that
touches a shared table (users, roles, audit_log, documents, document_chunks,
model_registry, connectors, notification_templates, city_profile,
exemption_rules) and mark it as the CivicCore baseline revision.

Migration-ordering contract (from CivicCore Extraction Spec section 14):

  1. CivicCore's migration runner is called FIRST by every consuming
     module's runner. The wrapper in each module is a thin shim around
     Alembic that calls `civiccore.migrations.run()` before applying its
     own revisions.

  2. For a fresh install, the sequence is:
        (a) civiccore_migrate upgrade head
        (b) <module>_migrate upgrade head     # records, clerk, code, zone, ...

  3. Order is enforced by Alembic's `depends_on` metadata on every
     module-side revision that touches a shared table. A module revision
     declares `depends_on = ("<civiccore_revision_id>",)` so a fresh DB
     cannot race the two runners.

  4. CivicCore NEVER imports from any module. Module migrations may
     reference shared tables, but the dependency arrow points one way:
     module --> civiccore.

  5. Shared-table schema changes are MAJOR CivicCore releases
     (semver-major). Minor and patch CivicCore releases never alter
     shared table schemas. See spec section 16.

This file deliberately does not configure a context, target_metadata, or
run_migrations_online() yet. Phase 1 will fill those in once the shared
models module is populated.
"""

# Phase 1 will add:
#   from alembic import context
#   from civiccore.models import Base
#   target_metadata = Base.metadata
#   def run_migrations_online() -> None: ...
#   def run_migrations_offline() -> None: ...
