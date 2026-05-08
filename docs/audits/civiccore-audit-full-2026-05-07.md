# CivicCore Audit Full - Release Recovery

Date: 2026-05-07
Repo: `CivicSuite/civiccore`
Mode: release-recovery audit
Audited checkout: local branch `quality/civiccore-audit-fixes`
Live baseline checked: `origin/main` at `a699814c6b97ff3ef13ecd9f04b5f4a2d76f7438`
Recovery branch head during audit: `2ce4f5be659c6e2f7f2f2d185f4b79fdf4be60c2` plus local recovery edits

## 1. Executive Audit

Static audit confidence: High for repository release posture, docs truth, test
layout, CI wiring, and release-gate behavior.

Runtime sign-off confidence: High for library tests and package install proof;
medium for browser/UX because CivicCore is a library and only the docs landing
page has a user-facing surface.

Verdict: CivicCore is a serious shared library with strong tests and release
provenance work, but the public `v1.0` posture needed recovery. The prior gate
could be invoked from WSL while silently selecting Windows `python.exe`, which
made the WSL evidence weaker than claimed. The repo also advertised
`Development Status :: 5 - Production/Stable`, which conflicts with the
suite-wide decision to treat current v1 labels as provisional until recovery
gates are complete.

Resolved during this pass:

- `REL-001`: Release gate preferred Windows Python inside WSL.
- `REL-002`: Package metadata advertised production/stable status.
- `DOC-001`: Public docs did not label `v1.0` as provisional during recovery.
- `QA-001`: Current-session browser QA evidence needed refresh for the changed
  docs landing page.

Open Blocker/Critical findings: none after fixes in this branch.

## 2. Audit Coverage Ledger

| Lane | Status | Evidence | Gap |
| --- | --- | --- | --- |
| Remote parity | Checked | `git fetch origin --prune`; local branch is ahead of `origin/main`. | Branch must be PR/merged before live parity is restored. |
| Local-vs-live commit truth | Checked | `HEAD_NOT_IN_MAIN` before recovery edits. | Live main still lacks this recovery patch until merge. |
| CI/workflow presence | Checked | `.github/workflows/ci.yml`, `cleanroom.yml`, `release-preflight.yml`, `release.yml`. | None. |
| Windows install path | Checked | Windows focused pytest passed; prior release gate passed with Windows Python. | Full final gate should run again before push. |
| Linux/Unix install path | Checked | WSL selected `.venv-wsl/bin/python3`, Linux Python 3.12, full release gate passed. | None. |
| Platform parity verdict | Checked | Windows focused tests plus WSL full gate. | CI must confirm after PR push. |
| First boot | Not applicable | CivicCore is a library, not an app server. | Downstream modules own first boot. |
| Required post-install steps | Checked | README/manual install path and clean-venv wheel install. | None. |
| Migrations | Checked | Baseline and LLM migration tests passed. | None. |
| Seed/bootstrap requirements | Not applicable | No app seed path. | Downstream modules own seeds. |
| Runtime dependency truth | Checked | Native WSL venv provisioned instead of skipping. | None. |
| Secrets and credentials | Checked | Tracked-file secret scan found no matches outside excluded evidence. | None. |
| Auth/session handling | Checked | Auth helper tests passed. | CivicCore does not own app sessions. |
| Authorization boundaries | Checked | Bearer/trusted-header helper tests passed. | Downstream modules must enforce roles. |
| Sensitive-data exposure | Checked | Library schemas reviewed through tests; no app response surface. | Downstream route schemas out of scope. |
| Audit/compliance logging | Checked | Audit primitive tests passed. | None. |
| External/admin surfaces | Not applicable | No app/admin server. | Downstream modules own runtime surfaces. |
| Connector completeness | Checked | Docs distinguish helpers from vendor adapters/write-back. | No vendor adapters shipped. |
| Connector docs truth | Checked | README/manual/docs list shipped vs unshipped connector behavior. | None. |
| Background jobs | Checked | Scheduling helper tests passed; docs state no scheduler runtime. | None. |
| Frontend critical journeys | Not applicable | No frontend app. | Docs landing page checked. |
| Loading/empty/error/partial states | Not applicable | Library docs page is static. | Downstream UIs own states. |
| Accessibility cues | Checked | Playwright focus sample on docs landing page. | Full formal a11y scan not run. |
| Docs truthfulness | Checked | Public status changed to provisional. | None. |
| Version consistency | Checked | `pyproject.toml`, `civiccore.__version__`, tests remain `1.0.0`; posture is provisional. | None. |
| Release artifact consistency | Partially checked | Local wheel build/install passed. | Existing GitHub release assets unchanged by this patch. |
| Test realism | Checked | 274 native WSL tests passed; provenance adversarial fixtures passed. | Downstream integration is module-owned. |
| Runtime/build/test verification | Checked | `scripts/verify-release.sh` passed under native WSL. | Final rerun before push required. |
| Browser verification | Checked | Playwright desktop/mobile docs QA passed. | None for library surface. |
| Prior audit challenge | Checked | External criticism applied: v1 labels provisional, real WSL proof, docs-source enforcement. | Org-wide recovery continues repo by repo. |

## 3. Claim Verification Matrix

| Claim | Source | Verdict | Evidence |
| --- | --- | --- | --- |
| CivicCore is a shared library, not an end-user app. | README, docs index, manual | True | Docs explicitly state this boundary. |
| `v1.0` exists as a published release/package version. | pyproject, release docs | True | Version remains `1.0.0`; release URL remains documented. |
| `v1.0` is production/stable. | Previous metadata/docs | False after recovery decision | Classifier changed to Beta and docs mark the label provisional. |
| WSL release verification uses Linux Python. | `scripts/verify-release.sh` | True after fix | Gate selected `.venv-wsl/bin/python3`; pytest reported platform linux. |
| Full local tests pass. | WSL release gate | True | 274 tests collected and passed. |
| Runtime install proof exists. | WSL release gate | True | Built wheel installed into clean venv and import smoke passed. |
| Browser QA is current for changed docs. | Playwright evidence | True | Desktop/mobile screenshots and summary added. |
| CivicCore ships vendor write-back, full ingestion, full search engine, notification queues, or legal determinations. | README/manual | False | Docs explicitly list these as unshipped. |

## 4. What The Dev Team Needs To Do Now

1. Keep the `v1.0` package version but do not promote it as production/stable
   until the suite-wide recovery program explicitly recertifies it.
2. Preserve the interpreter-order fix in `scripts/verify-release.sh`.
3. Push this recovery branch, open/merge a PR, and confirm GitHub CI is green.
4. Continue the same recovery process into downstream repos; CivicCore cannot
   certify product readiness for the apps that consume it.

## 5. Next-Sprint Watchlist

- Add a reusable repo-wide recovery gate script shared across CivicSuite repos.
- Consider a lightweight docs-source status schema so all modules can expose
  provisional/product-ready status consistently.
- Decide whether future CivicCore packaging should use a new patch version
  instead of editing docs around the existing `v1.0` tag.

## 6. Engineering Deep Dive

Checked: package metadata, release script, tests, workflows, public API smoke
coverage, migrations, auth helpers, connector helpers, scheduling, provenance,
and build/install path.

Finding `REL-001` was durable: the release script checked `python.exe` before
`python3`. In WSL, that allowed a Windows interpreter to satisfy a Linux proof.
Fix: prefer `python3`, then `python`, then `py`, then `python.exe`; add a
regression test that asserts `python3` is checked first.

## 7. Security And Authorization Deep Dive

Checked: tracked-file secret scan, auth helper tests, trusted-header tests,
host/config validation test coverage, encrypted JSON helpers.

No tracked secrets were found. Evidence-pack SBOM files include third-party
package descriptions and were excluded from the secret scan to avoid false
positives from upstream documentation strings.

## 8. UI/UX Deep Dive

Checked: `docs/index.html` because CivicCore has no app UI. Playwright ran
desktop and mobile checks. Provisional copy, install command, and not-end-user
app copy were visible. Console/page errors were empty. Keyboard focus reached
the expected links. Horizontal overflow was false.

## 9. Product/PM Deep Dive

The product boundary is now clearer: CivicCore is a dependency library. It can
be release-gated as a library, but it cannot prove that a city can run
CivicSuite. Downstream modules must earn their own product readiness.

## 10. Documentation Deep Dive

Docs now distinguish a published label from a re-earned product-ready claim.
README, text README, user manual, text manual, changelog, docs landing page,
and release recovery status were updated together.

## 11. Install / Bootstrap / Seeding Deep Dive

The install proof is strong for a library: the release gate builds a wheel,
installs into a fresh venv, checks exact version, and imports public surfaces.
No app seed path exists.

## 12. Version And Release Consistency Deep Dive

The version remains `1.0.0`; the posture changed. This is intentional because
the current recovery rule treats the existing label as provisional, not erased.
The package classifier no longer says production/stable.

## 13. Test Engineering Deep Dive

WSL full release verification passed under Linux Python 3.12 with 274 tests.
Focused Windows-side regression tests for metadata and workflow checks passed.
The script now has a test for native Unix Python preference.

## 14. Runtime QA Deep Dive

Runtime QA covered build/install and docs browser rendering. No server runtime
exists in CivicCore.

## 15. Cross-Cutting Synthesis

CivicCore’s architecture and tests are materially stronger than the public
release posture was. The key correction is honesty: keep the published artifact
available, but describe it as provisional during recovery and make the gates
prove what they claim.

## 16. Verification Gaps And Sign-Off Limits

- This audit does not recertify existing GitHub release assets; it prepares the
  repo truth/gates for a recovery PR.
- This audit does not certify downstream module compatibility.
- Final live parity requires PR merge and green CI on `main`.
