"""Prompt template resolution per ADR-0004 §7 (2-step DB algorithm).

Step 1 — App override:
    Look for an active row in prompt_templates with consumer_app=<requesting app>,
    template_name=<requested>, is_override=true, is_active=true.
    Highest version wins.

Step 2 — CivicCore default:
    Fall back to consumer_app='civiccore', template_name=<requested>,
    is_override=false, is_active=true. Highest version wins.

Step 3 — Missing:
    Raise PromptTemplateNotFoundError. No silent default.

Note: ADR-0004 §7 originally specified a 3-step algorithm with an in-memory
code-level override step between (1) and (2). That code-override layer is
deferred to a later release — the DB path satisfies the primary use case
(operators hot-fix prompts in production without redeploy). When a concrete
need for in-process overrides arises, this resolver will gain a third step
WITHOUT changing the existing two-step behavior.
"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from civiccore.llm.templates.exceptions import PromptTemplateNotFoundError
from civiccore.llm.templates.models import PromptTemplate

CIVICCORE_DEFAULT_APP = "civiccore"


async def resolve_template(
    session: AsyncSession,
    *,
    template_name: str,
    consumer_app: str,
) -> PromptTemplate:
    """Resolve a prompt template per the 2-step override algorithm.

    Args:
        session: Active SQLAlchemy AsyncSession.
        template_name: Logical template name (e.g., "exemption_review.system").
        consumer_app: Requesting application namespace (e.g., "civicrecords-ai").
            When set to "civiccore", step 1 is skipped (no self-override).

    Returns:
        The resolved PromptTemplate ORM row.

    Raises:
        PromptTemplateNotFoundError: When neither an app override nor a
            civiccore default is found. The error names both fields and tells
            the caller how to add the missing template.
    """
    # Step 1: App-specific override (skip if requester is civiccore itself)
    if consumer_app != CIVICCORE_DEFAULT_APP:
        stmt = (
            select(PromptTemplate)
            .where(
                PromptTemplate.consumer_app == consumer_app,
                PromptTemplate.template_name == template_name,
                PromptTemplate.is_override.is_(True),
                PromptTemplate.is_active.is_(True),
            )
            .order_by(PromptTemplate.version.desc())
            .limit(1)
        )
        result = await session.execute(stmt)
        row = result.scalar_one_or_none()
        if row is not None:
            return row

    # Step 2: CivicCore default
    stmt = (
        select(PromptTemplate)
        .where(
            PromptTemplate.consumer_app == CIVICCORE_DEFAULT_APP,
            PromptTemplate.template_name == template_name,
            PromptTemplate.is_override.is_(False),
            PromptTemplate.is_active.is_(True),
        )
        .order_by(PromptTemplate.version.desc())
        .limit(1)
    )
    result = await session.execute(stmt)
    row = result.scalar_one_or_none()
    if row is not None:
        return row

    # Step 3: Missing
    raise PromptTemplateNotFoundError(
        template_name=template_name,
        consumer_app=consumer_app,
    )


__all__ = ["resolve_template", "CIVICCORE_DEFAULT_APP"]
