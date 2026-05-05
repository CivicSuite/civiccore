# CO-8 CivicCore Claims Registry

Status: CO-8 load-bearing claim registry.

Verdict key:

- `Verified`: checked by command, committed evidence, live release asset, or
  tests in this session.
- `Policy-bound`: true as a governing rule, with future enforcement required
  in downstream sprints.

| ID | Claim | Source | Verdict | Evidence |
|---|---|---|---|---|
| CC-CLAIM-001 | CivicCore is a shared platform library, not an end-user app. | README, docs index | Verified | Package import smoke and no app first-boot path in CO-7/CO-8 checks. |
| CC-CLAIM-002 | `v0.22.1` is the first attested baseline release. | README, historical provenance policy | Verified | [`v0.22.1`](https://github.com/CivicSuite/civiccore/releases/tag/v0.22.1), `docs/ops/historical-provenance.md`. |
| CC-CLAIM-003 | Historical releases before the baseline are not attested baselines. | Historical provenance policy | Verified | [`docs/ops/civiccore-tier1-retrofit-ledger.md`](../../ops/civiccore-tier1-retrofit-ledger.md). |
| CC-CLAIM-004 | Release trust comes from `release-attestation.json` plus Sigstore bundle, not the GitHub badge alone. | README, policy, release notes | Verified | `scripts/verify-release-provenance.py`; CO-7 cosign verification returned `Verified OK`. |
| CC-CLAIM-005 | The freeze release is `civiccore-m1-freeze`. | Directive2, CO-7 closeout | Verified | [`civiccore-m1-freeze`](https://github.com/CivicSuite/civiccore/releases/tag/civiccore-m1-freeze). |
| CC-CLAIM-006 | The freeze release targets commit `3c4c34c...`. | Freeze attestation | Verified | CO-7 provenance verifier returned target commit `3c4c34ccd153eeae705a57139f6713c356328b6d`. |
| CC-CLAIM-007 | The freeze release did not become GitHub Latest. | CO-7 release workflow | Verified | GitHub latest API returned `v0.22.1` after freeze publication. |
| CC-CLAIM-008 | The public wheel can be installed from the release asset. | README install path | Verified | Fresh venv install from downloaded freeze wheel printed `published wheel import OK 0.22.1`. |
| CC-CLAIM-009 | The Git tag can be used as a freeze pin. | Directive2 CO-7 downstream rule | Verified | Fresh venv `pip install git+https://github.com/CivicSuite/civiccore@civiccore-m1-freeze` printed `git freeze pin install OK 0.22.1`. |
| CC-CLAIM-010 | CivicClerk can run against the freeze artifact. | CO-7 downstream pin feasibility | Verified | Temporary freeze-wheel harness: CivicClerk `553 passed`. |
| CC-CLAIM-011 | CivicCode can run against the freeze artifact. | CO-7 downstream pin feasibility | Verified | Temporary freeze-wheel harness: CivicCode `162 passed`. |
| CC-CLAIM-012 | Placeholder namespaces are not shipped contracts. | README, CO-7 ADRs | Verified | [`docs/adr/index.md`](../../adr/index.md), `tests/test_placeholder_adrs.py`. |
| CC-CLAIM-013 | Downstream modules must not depend on placeholder namespaces. | CO-7 ADRs | Policy-bound | CO-7 grep found only test guard references in CivicClerk/CivicCode. |
| CC-CLAIM-014 | CivicCore default runtime smoke can run without outbound network access. | CO-6 cleanroom | Verified | [`sovereignty-proof.md`](sovereignty-proof.md), offline smoke under Docker `--network none`. |
| CC-CLAIM-015 | CivicCore ships auth helpers for bearer and trusted-header role boundaries. | README, tests | Verified | `tests/test_auth_bearer.py` passed in `scripts/verify-release.sh`. |
| CC-CLAIM-016 | CivicCore ships connector retry/circuit-breaker primitives. | README, tests | Verified | `tests/test_connector_sync.py` passed in `scripts/verify-release.sh`. |
| CC-CLAIM-017 | CivicCore ships search normalization/access/RRF helpers, not a full search engine. | README, tests | Verified | `tests/test_search_helpers.py` passed; README states full engine remains planned. |
| CC-CLAIM-018 | CivicCore ships notice deadline/compliance helpers, not outbound delivery queues. | README, tests | Verified | `tests/test_notifications_notice.py` passed; README scopes delivery queues as unshipped. |
| CC-CLAIM-019 | CO-8/CO-9 SBOM files cover v0.22.1, freeze, the v1.0 release-candidate tree, and the final v1.0 package tree. | CO-8 evidence pack | Verified | Four `sbom-*.json` files generated from isolated installs with 83 packages each. |
| CC-CLAIM-020 | The final v1.0 SBOM is present in the evidence pack. | Directive2 CO-8/CO-9 sequence | Verified | [`sbom-v1.0-pip-inspect.json`](sbom-v1.0-pip-inspect.json), [`index.md`](index.md). |
| CC-CLAIM-021 | CivicCore v1.0 is the downstream productization release and v0.22.1 remains the first attested baseline release. | README, USER-MANUAL, docs index | Verified | `pyproject.toml`/`civiccore.__version__` are `1.0.0`; release notes and closeout point to the v1.0 tag while historical policy keeps v0.22.1 as baseline. |
