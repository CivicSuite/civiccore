"""Local task worker entry points for Townlight Core."""

from __future__ import annotations

from townlight_core.tasks.registry import get_task_handlers, register_task_handler

__all__ = ["get_task_handlers", "register_task_handler"]
