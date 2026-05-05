# ADR-0002: Defer `civiccore.exemptions`

Status: Accepted
Date: 2026-05-05
Sprint: CO-7 Spec Lockstep, Placeholder ADRs, and Freeze Line

## Context

`civiccore.exemptions` is reserved for a future public-records exemption engine.
The target capability includes rule evaluation, jurisdiction-specific source
citations, reviewer explanations, and optional LLM-assisted suggestions. None of
that policy-bearing behavior is implemented in the current CivicCore release
line.

An exemption engine affects legal review and public-records disclosure. Shipping
an incomplete or uncited shared contract at the freeze line would be worse than
leaving the namespace explicitly unshipped.

## Decision

Defer `civiccore.exemptions` to Phase 3. The namespace remains a placeholder
until a future CivicCore release ships tested rule contracts, source citation
requirements, reviewer-facing refusal behavior, documentation, and downstream
compatibility entries.

Explicit downstream consumption rule: no module depends on
`civiccore.exemptions` until it ships in a versioned CivicCore release artifact.
Modules that need exemption review before then must retain local, ADR-documented
behavior and must not present that behavior as CivicCore-provided.

## Consequences

- CO-7 freeze consumers must treat `civiccore.exemptions` as unimplemented.
- Compatibility reviews must flag imports, foreign keys, release claims, or
  docs that require `civiccore.exemptions`.
- Future extraction must include source-citation tests, refusal tests,
  jurisdiction drift tests, and reviewer override audit behavior before the
  namespace can be marked shipped.
