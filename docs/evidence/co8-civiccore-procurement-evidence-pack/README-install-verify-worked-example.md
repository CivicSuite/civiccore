# CO-8 README Install And Verify Worked Example

Status: CO-8 worked verification path for live CivicCore release assets.

This file records the auditor path for the attested baseline, freeze-line
release, and final `v1.0` downstream productization release.

## Verify The v1.0 Release

From a fresh clone of `CivicSuite/civiccore`, download the v1.0 release assets
into a single directory:

```bash
gh release download v1.0 \
  --repo CivicSuite/civiccore \
  --dir .tmp-v1-verify
cd .tmp-v1-verify
```

Verify Sigstore identity:

```bash
cosign verify-blob release-attestation.json \
  --bundle release-attestation.json.bundle \
  --certificate-identity "https://github.com/CivicSuite/civiccore/.github/workflows/release.yml@refs/tags/v1.0" \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```

Expected result:

```text
Verified OK
```

Verify checksums:

```bash
sha256sum -c SHA256SUMS.txt
```

Expected result:

```text
civiccore-1.0.0-py3-none-any.whl: OK
civiccore-1.0.0.tar.gz: OK
```

Verify release provenance from the repo root:

```bash
python scripts/verify-release-provenance.py v1.0 \
  --repo CivicSuite/civiccore \
  --attestation .tmp-v1-verify/release-attestation.json \
  --bundle .tmp-v1-verify/release-attestation.json.bundle \
  --artifacts-dir .tmp-v1-verify
```

Expected result:

```text
PASS: release provenance verified tag=v1.0
```

Install the published wheel:

```bash
python -m venv .tmp-civiccore-v1-install
. .tmp-civiccore-v1-install/bin/activate
python -m pip install https://github.com/CivicSuite/civiccore/releases/download/v1.0/civiccore-1.0.0-py3-none-any.whl
python -c "import civiccore; assert civiccore.__version__ == '1.0.0'; print(civiccore.__version__)"
```

Expected result:

```text
1.0.0
```

## Verify The Freeze Release

From a fresh clone of `CivicSuite/civiccore`, download the freeze release
assets into a single directory:

```bash
gh release download civiccore-m1-freeze \
  --repo CivicSuite/civiccore \
  --dir .tmp-freeze-verify
cd .tmp-freeze-verify
```

Verify Sigstore identity:

```bash
cosign verify-blob release-attestation.json \
  --bundle release-attestation.json.bundle \
  --certificate-identity "https://github.com/CivicSuite/civiccore/.github/workflows/release.yml@refs/tags/civiccore-m1-freeze" \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```

Expected result:

```text
Verified OK
```

Verify checksums:

```bash
sha256sum -c SHA256SUMS.txt
```

Expected result:

```text
civiccore-0.22.1-py3-none-any.whl: OK
civiccore-0.22.1.tar.gz: OK
```

Verify release provenance from the repo root:

```bash
python scripts/verify-release-provenance.py civiccore-m1-freeze \
  --repo CivicSuite/civiccore \
  --attestation .tmp-freeze-verify/release-attestation.json \
  --bundle .tmp-freeze-verify/release-attestation.json.bundle \
  --artifacts-dir .tmp-freeze-verify \
  --expected-target 3c4c34ccd153eeae705a57139f6713c356328b6d \
  --expected-tree 1e92d8b900b3d0134c4e8bc5b9133becff7822e6
```

Expected result:

```text
PASS: release provenance verified tag=civiccore-m1-freeze
```

Install the published wheel:

```bash
python -m venv .tmp-civiccore-install
. .tmp-civiccore-install/bin/activate
python -m pip install https://github.com/CivicSuite/civiccore/releases/download/civiccore-m1-freeze/civiccore-0.22.1-py3-none-any.whl
python -c "import civiccore; assert civiccore.__version__ == '0.22.1'; print(civiccore.__version__)"
```

Expected result:

```text
0.22.1
```

## Current-Session CO-8 Evidence

These current-session checks passed on Windows:

```text
cosign verify-blob ... -> Verified OK
sha256sum -c SHA256SUMS.txt -> wheel OK, sdist OK
verify-release-provenance.py civiccore-m1-freeze -> PASS
published wheel import OK 0.22.1
git freeze pin install OK 0.22.1
CivicClerk freeze harness -> 553 passed
CivicCode freeze harness -> 162 passed
```

## CO-9 Completion Record

CO-9 repeats this file's release-asset download, Sigstore, SHA256SUMS,
provenance, and install checks for the final `v1.0` release. The final v1.0
SBOM is recorded as `sbom-v1.0-pip-inspect.json`.
