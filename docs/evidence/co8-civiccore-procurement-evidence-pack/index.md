# CO-8 CivicCore Procurement Evidence Pack

Status: CO-8 evidence pack for outside-auditor review.

Sprint: CO-8 CivicCore Procurement Evidence Pack.

Repository: `CivicSuite/civiccore`.

Pack date: 2026-05-05.

Current live release anchors:

- Attested baseline release: [`v0.22.1`](https://github.com/CivicSuite/civiccore/releases/tag/v0.22.1)
- Freeze-line release: [`civiccore-m1-freeze`](https://github.com/CivicSuite/civiccore/releases/tag/civiccore-m1-freeze)
- Productization release: [`v1.0`](https://github.com/CivicSuite/civiccore/releases/tag/v1.0)
- Freeze workflow run: [`25405991283`](https://github.com/CivicSuite/civiccore/actions/runs/25405991283)
- Freeze target commit: `3c4c34ccd153eeae705a57139f6713c356328b6d`
- Freeze target tree: `1e92d8b900b3d0134c4e8bc5b9133becff7822e6`
- Freeze attestation identity:
  `https://github.com/CivicSuite/civiccore/.github/workflows/release.yml@refs/tags/civiccore-m1-freeze`
- Freeze attestation issuer: `https://token.actions.githubusercontent.com`

## How To Use This Pack

An outside auditor should be able to start here, verify the release artifacts,
then follow the claim registry to each load-bearing CivicCore claim. The pack is
not a marketing summary. It is the evidence table for procurement review.

Recommended order:

1. Verify the release attestation and checksums with
   [`README-install-verify-worked-example.md`](README-install-verify-worked-example.md).
2. Read the sprint preflight:
   [`preflight.md`](preflight.md).
3. Read the threat model:
   [`threat-model.md`](threat-model.md).
4. Verify the signed threat-model hash and signature:
   [`threat-model.md.sha256`](threat-model.md.sha256),
   [`threat-model.md.sig`](threat-model.md.sig), and
   [`threat-model-signing-public.pem`](threat-model-signing-public.pem).
5. Review the SBOM files:
   [`sbom-v0.22.1-pip-inspect.json`](sbom-v0.22.1-pip-inspect.json),
   [`sbom-civiccore-m1-freeze-pip-inspect.json`](sbom-civiccore-m1-freeze-pip-inspect.json),
   [`sbom-v1.0-pip-inspect.json`](sbom-v1.0-pip-inspect.json),
   and
   [`sbom-v1.0-rc-main-3c4c34c-pip-inspect.json`](sbom-v1.0-rc-main-3c4c34c-pip-inspect.json).
6. Review dependency licensing:
   [`license-manifest.md`](license-manifest.md) and
   [`license-manifest.json`](license-manifest.json).
7. Review incident drills:
   [`incident-response-runbook.md`](incident-response-runbook.md).
8. Review patch cadence:
   [`patch-cadence.md`](patch-cadence.md).
9. Review sovereignty proof:
   [`sovereignty-proof.md`](sovereignty-proof.md).
10. Review load-bearing claims:
   [`claims-registry.md`](claims-registry.md).
11. Check pack checksums:
   [`evidence-pack-manifest.json`](evidence-pack-manifest.json).

## Evidence Inventory

| Artifact | Purpose | Verification |
|---|---|---|
| `preflight.md` | Sprint-start repo, release, CI, frontend, and release-class state. | Compare with live GitHub state before audit. |
| `threat-model.md` | Versioned CivicCore procurement threat model. | Hash and SSH signature in this directory. |
| `incident-response-runbook.md` | Synthetic incident drills, including Sigstore and SHA256 failures. | Drill IDs are listed for CO-8 and CO-9 closeout reference. |
| `patch-cadence.md` | Security and provenance patch cadence record. | Links to PRs, workflow runs, and release pages. |
| `sovereignty-proof.md` | Network boundary and no-outbound runtime proof from CO-6. | References cleanroom manifest hashes and offline smoke logs. |
| `claims-registry.md` | README and release-surface claims mapped to evidence. | Each claim has a status and evidence pointer. |
| `license-manifest.*` | Dependency license manifest from generated SBOM data. | Generated from `pip inspect --local`. |
| `sbom-*.json` | SBOM-style package inventory for release anchors. | Generated from isolated installs with `pip inspect --local`. |
| `README-install-verify-worked-example.md` | Worked install and provenance verification path. | Uses live release assets and exact verifier commands. |

## CO-9 Completion Update

CO-8 landed before the authorized CO-9 `v1.0` publication, so the original pack
included `sbom-v1.0-rc-main-3c4c34c-pip-inspect.json` as a release-candidate
inventory. CO-9 adds `sbom-v1.0-pip-inspect.json` from the final `1.0.0`
package tree and records the release closeout in
[`../../ops/co-9-civiccore-v1-closeout.md`](../../ops/co-9-civiccore-v1-closeout.md).

The release-candidate SBOM remains in the pack as a sequencing record; the
final SBOM is the load-bearing `v1.0` package inventory.
