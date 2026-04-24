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


def upgrade_to_head(connection: "Connection") -> None:
    """Upgrade civiccore's migration chain to head using the supplied SQLAlchemy connection.

    Builds an Alembic Config pointing at civiccore's own `alembic.ini`, attaches
    the caller's live connection via `cfg.attributes["connection"]`, and runs
    `alembic upgrade head`. civiccore's `env.py` reads the attached connection
    on the normal code path so the operation participates in the caller's
    transaction scope.
    """
    cfg = alembic.config.Config(str(_ALEMBIC_INI))
    cfg.attributes["connection"] = connection
    command.upgrade(cfg, "head")


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
