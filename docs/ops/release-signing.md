# Release Signing and Provenance

CivicCore is now the canonical home for CivicSuite release-provenance gate
logic. Downstream modules should call `python -m civiccore.release_provenance`
or their local wrapper around `civiccore.release_provenance.main()` instead of
copying release checks by hand.

Release provenance is a pre-flight gate, not post-publication forensics. A
failing gate produces no release assets. There is no dev-process exemption, no
localhost identity exception, and no "fix it in the next release" path.

## Why This Gate Exists

GitHub release pages can show a "Verified" badge for the target commit even
when the release tag itself is lightweight or when the annotated tag object is
unsigned. That visual presentation is misleading for procurement review: the
commit may be GitHub-verified while the release pointer is not a verified tag
object. CivicSuite therefore verifies the GitHub tag ref, tag object, target
commit, committer identity, and release tree explicitly.

## Current v0.22.x Signing Model

The acceptable release shape is:

1. Merge the release PR through GitHub so the target commit is web-flow signed.
2. Create a GitHub-verified annotated release tag object that points at that
   verified target commit.
3. Run the adversarial fixture suite before checking the real tag:

   ```bash
   python scripts/verify-release-provenance.py --fixtures-dir tests/fixtures/release_provenance
   ```

4. Run the live provenance gate before publishing release assets:

   ```bash
   python scripts/verify-release-provenance.py vX.Y.Z \
     --repo CivicSuite/civiccore \
     --expected-target <verified-target-commit-sha> \
     --expected-tree <verified-release-tree-sha>
   ```

5. Publish the GitHub Release and assets only after the pre-flight gate passes.

The gate rejects lightweight tags, unsigned annotated tag objects, unsigned
target commits, non-GitHub web-flow committer identities, mismatched committer
fields, release-tree mismatch, and localhost/local tagger identities.

## CivicCore v0.22.0 Defect Statement

Current public artifact: `v0.22.0`

Defect an outside auditor can verify:

- GitHub tag ref `refs/tags/v0.22.0` points directly at commit
  `483a224aaf2ae08868bd4cd4caf842bfda97db94`.
- The target commit is GitHub-verified and uses key ID `B5690EEEBB952194`.
- The release tag is lightweight, so there is no verified annotated tag object.
- Therefore v0.22.0 fails the strengthened release provenance bar.

Reproducer:

```bash
python scripts/verify-release-provenance.py v0.22.0 --repo CivicSuite/civiccore
```

Expected output:

```text
FAIL: v0.22.0 is a lightweight tag pointing at commit 483a224aaf2ae08868bd4cd4caf842bfda97db94; create a signed annotated release tag instead.
```

This release is part of the Tier 1 live-surface correction window. Do not delete
or recreate it without explicit chat authorization for that specific release.

## Historical Baseline

The strengthened gate surfaced an org-wide historical provenance baseline
problem during the synthetic development phase: all 119 checked historical
CivicSuite release tags failed under the new bar, split between lightweight tags
and unsigned annotated tag objects. That is uncomfortable but useful evidence:
the gate is strict enough to catch real provenance defects before municipal
deployment. Current/live releases are corrected surgically; historical releases
are disclosed honestly rather than mass-deleted.
