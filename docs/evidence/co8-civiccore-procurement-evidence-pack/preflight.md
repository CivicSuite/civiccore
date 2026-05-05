# CO-8 Sprint Preflight

Sprint: CO-8 CivicCore Procurement Evidence Pack.

Date: 2026-05-05.

Affected repo: `CivicSuite/civiccore`.

## Local And Live State

| Item | State |
|---|---|
| Local branch at preflight | `main` before branch creation |
| CO-8 working branch | `docs/co-8-procurement-evidence-pack` |
| Dirty tree at preflight | Only untracked scratch/evidence directories from earlier local runs |
| Local `HEAD` | `3c4c34ccd153eeae705a57139f6713c356328b6d` |
| `origin/main` | `3c4c34ccd153eeae705a57139f6713c356328b6d` |
| Open CivicCore PRs | none |

The untracked scratch directories were not treated as product changes and were
not removed. CO-8 adds a curated evidence pack under
`docs/evidence/co8-civiccore-procurement-evidence-pack/`.

## Release State

| Release | State |
|---|---|
| Latest GitHub release | `v0.22.1` |
| Freeze release | `civiccore-m1-freeze` |
| Freeze release published | 2026-05-05T22:36:44Z |
| Freeze target commit | `3c4c34ccd153eeae705a57139f6713c356328b6d` |
| Freeze target tree | `1e92d8b900b3d0134c4e8bc5b9133becff7822e6` |
| Freeze Release workflow | `25405991283`, success |
| Main CI after CO-7 | `25405815870`, success |

## Required Checks Known At Preflight

- `bash scripts/verify-release.sh` must pass before push.
- CO-8 changes `docs/index.html`, so current-session browser evidence is
  required before commit.
- `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `LICENSE`, `.gitignore`,
  and `docs/index.html` already exist.
- CO-8 is documentation/evidence work and does not require release-class
  authorization unless release notes or published assets are edited.

## Known Drift And Sequencing Limits

- Final `v1.0` release assets do not exist yet. CO-8 includes a current
  release-candidate SBOM for commit `3c4c34c`; CO-9 must append the final
  `v1.0` SBOM after the release-class publication.
- Downstream productization lanes must use the CO-7 freeze as their trust
  anchor. CO-7 closeout proved CivicClerk and CivicCode can test against the
  freeze artifact through temporary harnesses.

## Frontend Surface

CO-8 changes only the static documentation landing page link list. Required
browser states for this static page:

- loading: document load completes;
- success: CO-8 evidence-pack link visible and correct;
- empty: not applicable, no data-backed empty state;
- error: no console or page errors;
- partial: not applicable, static page renders all sections from local HTML;
- desktop and mobile screenshots;
- keyboard focus, contrast, and overflow checks.

Browser evidence is stored in:

- `docs/browser-qa-co8-procurement-evidence-pack-desktop.png`
- `docs/browser-qa-co8-procurement-evidence-pack-mobile.png`
- `docs/browser-qa-co8-procurement-evidence-pack-summary.md`
