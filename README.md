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

**Early scaffold.** This repository currently contains the v0.1 package
skeleton (Phase 0 of the extraction). Subsystems are empty `__init__.py`
files; nothing functional ships yet. The first functional release —
**v0.1.0** — lands with **Phase 1** (shared models + audit chain). See
the CivicCore Extraction Spec section 12 for the phased rollout.

## Install

Once published to PyPI:

```bash
pip install civiccore
```

For now (pre-release), install from a clone:

```bash
git clone https://github.com/CivicSuite/civiccore.git
cd civiccore
pip install -e .[dev]
```

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
