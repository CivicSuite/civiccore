# CO-8 CivicCore Patch Cadence Evidence

Status: CO-8 security and provenance patch-cadence record.

Scope: CivicCore release-provenance hardening and downstream trust boundary
work completed on 2026-05-05.

## Cadence Summary

| Sprint | Evidence | Security or trust impact |
|---|---|---|
| CO-2c | [`v0.22.1`](https://github.com/CivicSuite/civiccore/releases/tag/v0.22.1) | First attested CivicCore baseline with Sigstore bundle and checksums. |
| CO-3 | [`docs/ops/civiccore-tier1-retrofit-ledger.md`](../../ops/civiccore-tier1-retrofit-ledger.md) | Historical CivicCore release-tag provenance decisions are ledgered instead of rewritten. |
| CO-4 | [`docs/ops/co-4-cross-module-retrofit-report.md`](../../ops/co-4-cross-module-retrofit-report.md) | Cross-module pre-gate releases are explicitly recorded. |
| CO-5 | [`docs/ops/historical-provenance.md`](../../ops/historical-provenance.md) | Disclosure became operative provenance policy. |
| CO-6 | [`docs/ops/cleanroom-harness.md`](../../ops/cleanroom-harness.md) | Cleanroom verification harness proves release, Sigstore, SHA256SUMS, and offline runtime paths. |
| CO-7 | [`civiccore-m1-freeze`](https://github.com/CivicSuite/civiccore/releases/tag/civiccore-m1-freeze) | Freeze-line release is signed and verified for downstream productization. |
| CO-8 | This evidence pack | Procurement evidence links load-bearing claims to verification artifacts. |
| CO-9 | [`v1.0`](https://github.com/CivicSuite/civiccore/releases/tag/v1.0) | Downstream productization release adds final SBOM and closeout report. |

## Release And CI Evidence

- `v0.22.1` release published: 2026-05-05T16:23:36Z.
- `civiccore-m1-freeze` release published: 2026-05-05T22:36:44Z.
- CO-7 freeze Release workflow run:
  <https://github.com/CivicSuite/civiccore/actions/runs/25405991283>
- CO-7 main CI run:
  <https://github.com/CivicSuite/civiccore/actions/runs/25405815870>

## Security-Relevant Checks

The current gate checks:

- full test suite through `scripts/verify-release.sh`;
- release-provenance fixture suite;
- exact GitHub Actions OIDC workflow identity;
- tag ref and target commit;
- target tree;
- release asset hashes;
- Sigstore bundle verification;
- SHA256SUMS verification; and
- fresh virtualenv wheel-install smoke.

## CO-9 Closeout

CO-9 publishes the final v1.0 release and appends the final v1.0 SBOM to this
evidence pack. The release-class operation creates the final tag and assets;
post-publication verification follows the commands in
[`README-install-verify-worked-example.md`](README-install-verify-worked-example.md).
