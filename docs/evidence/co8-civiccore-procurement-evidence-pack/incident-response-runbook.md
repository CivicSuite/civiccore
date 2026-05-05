# CO-8 CivicCore Incident Response Runbook

Status: CO-8 synthetic incident drills for release and procurement evidence.

Owner area: CivicCore release steward.

Escalation rule: if a public release artifact or trust artifact is wrong,
pause downstream pinning claims until the public state is verified or a
freshly authorized correction is complete.

## IR-CO8-001: Sigstore Attestation Fails Verification Post-Publish

Trigger:

- `cosign verify-blob release-attestation.json --bundle release-attestation.json.bundle`
  fails for a published release.
- Or `scripts/verify-release-provenance.py` rejects the bundle identity,
  issuer, target commit, target tree, or artifact hashes.

Immediate actions:

1. Stop all release-promotion language for the affected tag.
2. Record the release tag, asset URLs, failing command, command output, and
   current GitHub Release asset list.
3. Confirm whether the tag, release assets, or release notes were edited after
   publication.
4. Do not delete, move, replace, or upload release assets without fresh
   release-class authorization.
5. File a failure report under the sprint ID that owns the release.

Fix-forward options:

- If no public release assets were created, rerun the release workflow after
  fresh authorization.
- If public assets exist and are wrong, request explicit authorization for the
  exact edit, replacement, deletion, or corrective release.
- If the failure is an auditor environment problem, publish the exact auditor
  dependency fix and keep the original release assets unchanged.

Exit criteria:

- The documented verification commands pass from a fresh asset download.
- The failure report records the visible state before and after correction.
- The claims registry points only to the corrected evidence.

## IR-CO8-002: SHA256SUMS Mismatch On Published Wheel

Trigger:

- `sha256sum -c SHA256SUMS.txt` fails for the wheel or sdist.
- Or a downloaded asset hash differs from `release-attestation.json`.

Immediate actions:

1. Treat the release as blocked.
2. Stop downstream package pin updates to that release.
3. Preserve the downloaded assets, checksum file, and command output as
   evidence.
4. Compare the GitHub Release asset list to the release workflow upload list.
5. Do not replace assets without fresh release-class authorization.

Fix-forward options:

- Fresh authorization to replace the wrong assets and update checksums.
- Fresh authorization to publish a corrected release tag if replacement would
  obscure the audit trail.
- Fresh authorization to mark the release as superseded if the tag should not
  be trusted.

Exit criteria:

- A fresh download validates with `sha256sum -c`.
- Provenance verifier validates the same asset hashes.
- Release notes or evidence docs explain any supersession.

## IR-CO8-003: Freeze Release Marked Latest By Mistake

Trigger:

- GitHub latest release API returns `civiccore-m1-freeze` after freeze
  publication.

Immediate actions:

1. Record `gh api repos/CivicSuite/civiccore/releases/latest --jq .tag_name`.
2. Do not edit release metadata without fresh release-class authorization.
3. Request narrow authorization to reset the latest pointer or edit release
   metadata.

Exit criteria:

- Latest release returns the intended versioned release tag.
- The freeze release remains available and verifiable but is not the Latest
  pointer.

CO-7 observed state:

- Latest release remained `v0.22.1`.
- Freeze release was published with `--latest=false`.

## IR-CO8-004: Evidence Pack Drift After Merge

Trigger:

- `evidence-pack-manifest.json` hash does not match a checked-out evidence
  file.
- Or docs link to release assets that no longer exist.

Immediate actions:

1. Stop using the evidence pack as a procurement artifact.
2. Regenerate affected generated files from current release assets.
3. Re-run release verification commands.
4. Open a doc-class correction PR unless the correction touches release
   assets, release notes, or tags.

Exit criteria:

- Evidence pack manifest matches.
- Verification commands pass.
- Changelog records the correction.
