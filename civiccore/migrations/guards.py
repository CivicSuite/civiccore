"""Idempotent Alembic operation helpers. These wrap alembic.op.* calls with 'skip if already exists' semantics so civiccore's baseline migration and records' 14 guarded migrations can all be re-run against a database that already contains the shared schema."""

from __future__ import annotations

from typing import Any

import alembic.op as op
import sqlalchemy as sa
from sqlalchemy.engine import Inspector


def _inspector() -> Inspector:
    """Return a fresh SQLAlchemy Inspector bound to the current Alembic connection."""
    return sa.inspect(op.get_bind())


def idempotent_create_table(name: str, *columns: Any, **kwargs: Any) -> None:
    """op.create_table that no-ops if the table already exists.

    Used by civiccore's baseline migration and by guarded records migrations that
    create shared tables (e.g. `users`, `data_sources`). If the table is already
    present in the database, the create is skipped; otherwise it proceeds normally.
    """
    inspector = _inspector()
    if inspector.has_table(name):
        return
    op.create_table(name, *columns, **kwargs)


def idempotent_add_column(table: str, column: Any, **kwargs: Any) -> None:
    """op.add_column that no-ops if the column already exists.

    If the target table itself does not exist, returns silently — the upstream
    migration (or civiccore baseline) is responsible for creating it. If the
    table exists and the column is already present, skip. Otherwise add it.
    """
    inspector = _inspector()
    if not inspector.has_table(table):
        # Upstream migration will handle table creation; nothing to add to.
        return
    existing = {col["name"] for col in inspector.get_columns(table)}
    if column.name in existing:
        return
    op.add_column(table, column, **kwargs)


def idempotent_alter_column(
    table: str,
    column: str,
    *,
    existing_type: Any = None,
    nullable: bool | None = None,
    server_default: Any = None,
    new_column_name: str | None = None,
    **kwargs: Any,
) -> None:
    """op.alter_column that introspects current state before applying.

    Applies the alter only when a concrete difference is detected:
      - `nullable` is specified AND the current column's nullable != requested, OR
      - `new_column_name` is specified AND it differs from `column`.

    `existing_type` and `server_default` are passed through to `op.alter_column`
    but are NOT used as the diff trigger — type/default deep-comparison is too
    brittle across dialects. Those alters are the caller's responsibility to
    schedule once by migration history; this guard exists to absorb repeat runs.

    If the table or column does not exist, returns silently.
    """
    inspector = _inspector()
    if not inspector.has_table(table):
        return

    cols = {col["name"]: col for col in inspector.get_columns(table)}
    current = cols.get(column)
    if current is None:
        return

    should_apply = False
    if nullable is not None and bool(current.get("nullable")) != bool(nullable):
        should_apply = True
    if new_column_name is not None and new_column_name != column:
        should_apply = True

    if not should_apply:
        return

    alter_kwargs: dict[str, Any] = dict(kwargs)
    if existing_type is not None:
        alter_kwargs["existing_type"] = existing_type
    if nullable is not None:
        alter_kwargs["nullable"] = nullable
    if server_default is not None:
        alter_kwargs["server_default"] = server_default
    if new_column_name is not None:
        alter_kwargs["new_column_name"] = new_column_name

    op.alter_column(table, column, **alter_kwargs)


def has_table(name: str) -> bool:
    """Thin public wrapper returning whether the named table exists in the current DB."""
    return _inspector().has_table(name)
