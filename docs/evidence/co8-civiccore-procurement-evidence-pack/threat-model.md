# CO-8 CivicCore Threat Model

Version: 1.

Status: signed CO-8 threat model for CivicCore procurement review.

Repository: `CivicSuite/civiccore`.

Scope: CivicCore v0.22.1, `civiccore-m1-freeze`, and the current v1.0 release
candidate tree at commit `3c4c34ccd153eeae705a57139f6713c356328b6d`.

## System Boundary

CivicCore is a shared Python platform library. It is not an end-user municipal
application. Downstream CivicSuite modules import CivicCore primitives for
migrations, LLM provider abstraction, audit chains, provenance, manifests,
export bundles, city profiles, auth helper contracts, connector retry and
circuit-breaker helpers, search helper contracts, scheduling helpers,
notification deadline helpers, onboarding profile helpers, release provenance,
and test/evidence utilities.

CivicCore does not own a production web server, resident portal, clerk
workflow UI, municipal database, or vendor connector credential store in this
release line. Those are downstream module responsibilities.

## Protected Assets

| Asset | Why it matters | Primary control |
|---|---|---|
| Release artifacts | Downstream modules build from released wheels and sdists. | GitHub Release, SHA256SUMS, Sigstore attestation, release workflow gate. |
| Release attestation | This is the trust artifact for a tag and target tree. | `release-attestation.json` plus cosign bundle and exact OIDC identity. |
| Audit-chain primitives | Downstream modules depend on tamper-evident audit rows. | Unit tests for hash chains and persisted audit verification. |
| Manifest and export helpers | Downstream evidence bundles rely on checksum correctness. | Manifest and export-bundle validation tests. |
| Auth helper contracts | Downstream staff routes depend on fail-closed helper behavior. | Bearer and trusted-header tests with actionable failure modes. |
| Connector config and host validation | Prevents unsafe connector targets and credential leakage. | Host validation, encrypted JSON, and config validation tests. |
| Placeholder namespace boundary | Prevents downstream modules from depending on unshipped packages. | CO-7 ADRs and placeholder tests. |
| Evidence pack integrity | Procurement reviewers need stable claim-to-evidence mapping. | Evidence pack checksums plus signed threat model. |

## Threats And Controls

### T1: Unsigned Or Ambiguous Release Provenance

Threat: an operator treats a GitHub "Verified" badge or tag pointer as enough
proof of release integrity.

Controls:

- `release-attestation.json` schema version 1.
- Cosign bundle verification against exact GitHub Actions OIDC identity.
- `scripts/verify-release-provenance.py` checks repo, tag, tag ref, target
  commit, target tree, artifact hashes, identity, and issuer.
- Release workflow verifies provenance before publication.
- Historical provenance policy warns that pre-baseline releases are not
  attested baselines.

Residual risk: auditors must run the documented verification commands. The
project cannot make an unaudited downstream mirror safe by documentation alone.

### T2: Artifact Tampering After Publication

Threat: a wheel, sdist, checksum file, or attestation asset is replaced or
partially uploaded.

Controls:

- `SHA256SUMS.txt` must verify the wheel and sdist.
- The release attestation carries artifact hashes.
- The provenance verifier checks downloaded assets against the attestation.
- Directive2 requires fresh authorization for replacement or corrective
  publication.

Residual risk: GitHub Release metadata is mutable by authorized maintainers, so
auditors must verify the live assets instead of trusting release-page prose.

### T3: Downstream Reliance On Placeholder Namespaces

Threat: CivicClerk, CivicCode, or another module imports a placeholder package
and silently depends on unimplemented behavior.

Controls:

- CO-7 ADRs for `civiccore.catalog`, `civiccore.exemptions`, and
  `civiccore.scaffold`.
- Tests assert ADR presence and package docstrings.
- Downstream grep checks found only test guard references in CivicClerk and
  CivicCode during CO-7 closeout.

Residual risk: future downstream sprints must keep placeholder scans in their
compatibility checks.

### T4: Unexpected Outbound Runtime Network Calls

Threat: the default CivicCore runtime path performs network calls after
installation, weakening sovereignty and auditability claims.

Controls:

- CO-6 cleanroom harness runs offline runtime smoke under Docker
  `--network none`.
- Cleanroom manifest records `offline-runtime-smoke` and
  `offline-release-provenance-fixtures` as PASS.
- Local-first provider and connector tests mock network paths.

Residual risk: live optional providers and future connector adapters must be
tested in downstream modules before production deployment.

### T5: Secrets Or Sensitive Config Leakage

Threat: helper APIs expose tokens, connector credentials, or secret-bearing
configuration in response bodies, logs, or evidence bundles.

Controls:

- Encrypted JSON helper tests.
- Connector host and URL validation tests.
- Secret placeholder and common-password rejection tests.
- Cleanroom evidence uses release assets, not deployment credentials.

Residual risk: downstream modules must redact their own tenant-specific
configuration and logs.

### T6: Dependency Or License Drift

Threat: a release depends on a package set or license surface that differs
from what procurement reviewers were given.

Controls:

- CO-8 SBOM files generated from isolated installs for `v0.22.1`,
  `civiccore-m1-freeze`, and the current v1.0 release-candidate tree.
- CO-8 license manifest generated from those SBOM files.
- CO-9 must append the final v1.0 SBOM after release publication.

Residual risk: package indexes change over time. Auditors should treat the
committed SBOM as the evidence for this review and regenerate it during CO-9.

## Verification Checklist

An auditor should verify:

1. `cosign verify-blob` succeeds for the freeze release attestation.
2. `sha256sum -c SHA256SUMS.txt` succeeds for the freeze wheel and sdist.
3. `python scripts/verify-release-provenance.py civiccore-m1-freeze ...`
   succeeds against downloaded release assets.
4. `bash scripts/verify-release.sh` passes on the repo checkout.
5. The CO-7 placeholder ADR tests pass.
6. The CO-8 evidence pack manifest hashes match the checked-out files.
