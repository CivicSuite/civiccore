# Historical Provenance Disclosure Draft

Status: draft for auditor review. This document is not yet the umbrella
CivicSuite disclosure and must not be treated as published policy until it lands
through the authorized CivicSuite documentation path.

## Summary

CivicSuite strengthened its release provenance model during the synthetic
development phase. The prior model relied on GitHub-native release pages and
tag references. A backfill scan found that historical releases were either
lightweight tags or unsigned annotated tag objects. GitHub's release UI can show
a "Verified" badge for the target commit, but that visual signal does not mean
the tag object itself is signed or verified.

The new model treats tags as release pointers and makes a Sigstore-signed
`release-attestation.json` the trust artifact. Releases after the baseline date
must include the attestation, cosign bundle, artifact checksums, evidence bundle
hashes, and an exact per-repo/per-tag verification command.

## Historical State

- Historical releases before the baseline date were produced under a weaker
  GitHub-native provenance model.
- Those releases are not retroactively deleted or rewritten.
- Current/latest live-surface releases receive additive attestations only after
  per-release authorization.
- Cities and procurement reviewers should pin to post-baseline releases when
  procurement-grade provenance is required.

## New Baseline

A post-baseline release is independently verifiable when:

- the target commit is GitHub-verified,
- the tag ref points at the attested commit/tree,
- the release assets match `SHA256SUMS.txt`,
- `release-attestation.json` follows schema version 1,
- the attestation is signed by the exact expected GitHub Actions OIDC workflow
  identity for the repo and tag,
- the cosign bundle verifies with the documented issuer and trust roots, and
- release notes include the exact verification command.

## Audit Interpretation

This disclosure does not minimize the prior state. It records a baseline shift:
the project found that its previous release-page verification signal was
insufficient, stopped destructive corrections, adopted a verifiable attestation
model, and preserved historical releases instead of rewriting the record.
