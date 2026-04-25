"""
civiccore.llm.registry — ORM model and Pydantic schemas for model_registry.

Public exports:

- ``ModelRegistry``        — SQLAlchemy ORM model (maps to the model_registry table).
- ``ModelRegistryCreate``  — Pydantic schema for POST (create).
- ``ModelRegistryRead``    — Pydantic schema for GET responses (ORM-compatible).
- ``ModelRegistryUpdate``  — Pydantic schema for PATCH (partial update).

Service-layer helpers (``get_active_model``, ``get_active_model_context_window``)
will be added in Phase 2 Step 3d via ``civiccore.llm.registry.service``.
"""

from civiccore.llm.registry.models import ModelRegistry
from civiccore.llm.registry.schemas import (
    ModelRegistryCreate,
    ModelRegistryRead,
    ModelRegistryUpdate,
)

__all__ = [
    "ModelRegistry",
    "ModelRegistryCreate",
    "ModelRegistryRead",
    "ModelRegistryUpdate",
]
