# ADR-0001: Defer `civiccore.catalog`

Status: Accepted
Date: 2026-05-05
Sprint: CO-7 Spec Lockstep, Placeholder ADRs, and Freeze Line

## Context

`civiccore.catalog` exists only as a reserved package name. The long-term
platform vision includes an installed-module catalog, municipal-system catalog,
connector directory, and recommendation surface, but the current CivicCore
release line does not implement those behaviors.

Shipping a partial catalog API at the CO-7 freeze would create a false contract
for downstream modules. The freeze must be a point where downstream consumers
can distinguish shipped primitives from planned platform behavior.

## Decision

Defer `civiccore.catalog` to Phase 4. The namespace remains a placeholder until
a future CivicCore release ships a tested catalog contract, documentation, and
compatibility-matrix entry.

Explicit downstream consumption rule: no module depends on
`civiccore.catalog` until it ships in a versioned CivicCore release artifact.
Downstream modules may keep local catalog or module-registry bridges only when
their own ADR records the bridge, the extraction plan, and the CivicCore release
that will replace it.

## Consequences

- CO-7 freeze consumers must treat `civiccore.catalog` as unimplemented.
- Compatibility reviews must flag imports, foreign keys, README claims, or test
  fixtures that make `civiccore.catalog` a required dependency.
- The future catalog extraction must include tests for empty city profiles,
  unknown vendor systems, unsupported module IDs, and actionable operator copy
  before the namespace can be marked shipped.
