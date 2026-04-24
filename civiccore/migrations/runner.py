"""Programmatic entry point for civiccore migrations. Consumed by records' env.py (Phase 1 Part B) so records' alembic upgrade automatically brings civiccore up to head first."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import alembic.config
from alembic import command
from alembic.runtime.migration import MigrationContext

if TYPE_CHECKING:
    from sqlalchemy.engine import Connection


_ALEMBIC_INI = Path(__file__).with_name("alembic.ini")


def upgrade_to_head(connection: "Connection | None" = None) -> None:
    """Upgrade civiccore's migration chain to head.

    **Always opens its own synchronous SQLAlchemy connection from the
    DATABASE_URL environment variable**, ignoring any ``connection`` passed
    by the caller. The signature retains ``connection`` as an optional kwarg
    only for source-compat with consumers that pass it; the value is
    intentionally unused.

    Why: ``alembic.command.upgrade`` installs a process-global context proxy
    via ``alembic.context._install_proxy``. When invoked from inside another
    active env.py (e.g., civicrecords' env.py wiring), exiting civiccore's
    EnvironmentContext destroys the caller's proxy state, causing
    ``AttributeError: 'NoneType' object has no attribute 'configure'`` when
    the caller's env.py continues. Opening a separate connection keeps
    civiccore's alembic invocation cleanly isolated.

    Trade-off: civiccore commits independently of the caller's transaction.
    The baseline is idempotent, so a partial-state restart produces the
    same end-state — acceptable per ADR-0003 §"Three deployment scenarios".

    Requires ``DATABASE_URL`` env var to be set. The URL may use any psycopg2
    or asyncpg dialect; civiccore normalizes to ``postgresql+psycopg2`` for
    its own sync alembic invocation.
    """
    import os
    from sqlalchemy import create_engine

    url = os.environ.get("DATABASE_URL")
    if url is None:
        raise RuntimeError(
            "civiccore.migrations.runner.upgrade_to_head requires "
            "DATABASE_URL to be set; civiccore opens its own connection "
            "to avoid nesting inside the caller's alembic context."
        )

    # Normalize to sync psycopg2 driver — civiccore alembic is sync-only
    sync_url = (
        url.replace("postgresql+asyncpg", "postgresql+psycopg2")
           .replace("postgres+asyncpg", "postgresql+psycopg2")
           .replace("postgresql+asyncpg", "postgresql+psycopg2")
    )
    if sync_url.startswith("postgresql://") or sync_url.startswith("postgres://"):
        sync_url = sync_url.replace("postgresql://", "postgresql+psycopg2://", 1)
        sync_url = sync_url.replace("postgres://", "postgresql+psycopg2://", 1)

    cfg = alembic.config.Config(str(_ALEMBIC_INI))
    engine = create_engine(sync_url)
    try:
        with engine.connect() as conn:
            cfg.attributes["connection"] = conn
            command.upgrade(cfg, "head")
    finally:
        engine.dispose()


def current_revision(connection: "Connection") -> str | None:
    """Return civiccore's current Alembic revision on this connection, or None if unstamped.

    Reads from the `alembic_version_civiccore` version table so it does not
    collide with records' own `alembic_version` table in the same database.
    """
    ctx = MigrationContext.configure(
        connection,
        opts={"version_table": "alembic_version_civiccore"},
    )
    return ctx.get_current_revision()
