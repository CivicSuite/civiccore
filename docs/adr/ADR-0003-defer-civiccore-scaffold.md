# ADR-0003: Defer `civiccore.scaffold`

Status: Accepted
Date: 2026-05-05
Sprint: CO-7 Spec Lockstep, Placeholder ADRs, and Freeze Line

## Context

`civiccore.scaffold` is reserved for a future module generator and bootstrap
workflow. The planned CLI would create a working CivicSuite module skeleton with
migrations, documentation gates, authentication placeholders, QA hooks, and
suite registration. The current CivicCore release line does not ship that CLI or
the generated template contract.

The scaffold behavior is high leverage: a weak generator would multiply bad
defaults into every later module. It should not be treated as shipped until the
template, tests, and documentation gates are stable.

## Decision

Defer `civiccore.scaffold` to Phase 4. The namespace remains a placeholder until
a future CivicCore release ships a tested scaffold command, template contract,
documentation, and compatibility-matrix entry.

Explicit downstream consumption rule: no module depends on
`civiccore.scaffold` until it ships in a versioned CivicCore release artifact.
Module bootstrapping work before that release must be local or umbrella-owned
and must not require the placeholder namespace.

## Consequences

- CO-7 freeze consumers must treat `civiccore.scaffold` as unimplemented.
- Compatibility reviews must flag imports, setup scripts, READMEs, or CI jobs
  that require `civiccore.scaffold`.
- Future scaffold extraction must include a generated-module boot test, docs
  artifact gate, CI template check, and placeholder-free configuration test
  before the namespace can be marked shipped.
