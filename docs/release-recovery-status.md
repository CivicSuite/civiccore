# CivicCore Release Recovery Status

Date: 2026-05-07
Repo: `CivicSuite/civiccore`

## Current Verdict

`v1.0` exists as a published GitHub release and package version, but it is
treated as provisional during the CivicSuite release-recovery pass. Do not use
the label as a public production/stable claim until the recovery gate evidence
below is complete and current.

## Recovery Gates

| Gate | Current status | Evidence |
| --- | --- | --- |
| Public product-ready claim freeze | Passing | README, text README, user manual, docs landing page, and package classifier now avoid production/stable promotion. Claim scan only found negative/provisional wording. |
| Runtime install proof | Passing | `scripts/verify-release.sh` builds a wheel and installs it into a clean virtualenv. Verified in native WSL on 2026-05-07. |
| Native WSL/Linux proof | Passing | Release gate selected `.venv-wsl/bin/python3`, ran on Linux Python 3.12, collected 274 tests, and passed. |
| Security scan | Passing | Tracked-file secret scan found no matches outside ignored evidence/scratch surfaces. |
| Docs-source consistency | Passing | Version and release posture are tested from source files. |
| Mock-vs-production labeling | Passing for library scope | README and user manual distinguish shipped helpers from placeholders and unshipped platform behaviors. |
| Browser/user-flow QA | Passing | CivicCore is a library. Playwright checked the docs landing page at desktop and mobile widths, with no console/page errors, visible provisional copy, keyboard focus samples, and no horizontal overflow. |

## Sign-Off Boundary

CivicCore is a shared library, not an end-user municipal app. It cannot by
itself prove that a city can run the CivicSuite product family. Downstream
modules must re-earn their own release status with module-specific runtime,
UX, integration, security, and documentation gates.
