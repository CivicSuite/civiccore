# CivicCore Architecture Decision Records

CivicCore ADRs record module-scoped platform decisions. Cross-module decisions
that bind more than one repository remain in the umbrella `CivicSuite`
architecture ADR index.

## Placeholder Namespace Deferrals

These CO-7 ADRs define the placeholder namespace boundary for the freeze line:

- [ADR-0001: Defer `civiccore.catalog`](ADR-0001-defer-civiccore-catalog.md)
- [ADR-0002: Defer `civiccore.exemptions`](ADR-0002-defer-civiccore-exemptions.md)
- [ADR-0003: Defer `civiccore.scaffold`](ADR-0003-defer-civiccore-scaffold.md)

Rule: no downstream module may import, foreign-key to, document as required, or
otherwise depend on a placeholder namespace until that namespace ships in a
versioned CivicCore release artifact and the downstream compatibility matrix is
updated to name that release.
