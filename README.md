# CivicCore

Shared platform package for the
[CivicSuite](https://github.com/CivicSuite/civicsuite) open-source
municipal operations suite.

## What this is

CivicCore is the Python package every CivicSuite module depends on for
authentication, audit logging, LLM access, document ingestion, hybrid
search, connectors, notifications, onboarding, the 50-state public-records
exemption engine, and sovereignty verification. It is extracted from the
production CivicRecords AI codebase per the CivicCore Extraction Spec, and
is consumed today by CivicRecords AI; CivicClerk, CivicCode, and CivicZone
will consume it as they ship.

## Status

**Phase 1 shipped.** `v0.1.0` is the first functional CivicCore release:
the migration runner, idempotent guards, and the `civiccore_0001_baseline_v1`
shared-schema baseline extracted from CivicRecords AI. See the CivicCore
Extraction Spec section 12 for the phased rollout.

## Install

From the GitHub release wheel:

```bash
pip install https://github.com/CivicSuite/civiccore/releases/download/v0.1.0/civiccore-0.1.0-py3-none-any.whl
```

Each GitHub release also publishes `SHA256SUMS.txt` alongside the wheel and
sdist. Verify the checksum before promoting a release artifact into a downstream
module or internal package mirror.

For development from a clone:

```bash
git clone https://github.com/CivicSuite/civiccore.git
cd civiccore
pip install -e .[dev]
```

PyPI publication can come later; `v0.1.0` is distributed first as a versioned
GitHub release artifact so CivicRecords AI can stop depending on a Git SHA pin.
The tag-driven release workflow runs `scripts/verify-release.sh` before
publishing so the shipped artifact has already passed pytest, ruff,
docs/version checks, a local build, and a clean-virtualenv wheel-install smoke
test.

## Public API surface

CivicCore's v0.1 public API is deliberately lean. The full list of
exported symbols — which is **stable across the v0.x series** per the
spec's semver policy — is published in **Appendix A of the CivicCore
Extraction Spec** in
[CivicSuite/civicsuite](https://github.com/CivicSuite/civicsuite).
Refer to that document; this README does not duplicate the list, so the
two cannot drift.

## Compatibility

Every CivicSuite module's README declares a CivicCore version range
(e.g. `civiccore >= 0.1, < 0.2`). The suite-wide compatibility matrix —
which module versions work with which CivicCore versions — is maintained
at
[CivicSuite/civicsuite/docs/compatibility/](https://github.com/CivicSuite/civicsuite/tree/main/docs/compatibility).

## License

[Apache License 2.0](LICENSE).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md), including the decision tree for
where to file a bug across the CivicSuite multi-repo layout.
