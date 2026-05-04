from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from civiccore.release_provenance import build_release_attestation, canonical_json_bytes


REPO_ROOT = Path(__file__).resolve().parents[1]
PROVENANCE_SCRIPT = REPO_ROOT / "scripts" / "verify-release-provenance.py"
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures" / "release_provenance"


def test_adversarial_release_provenance_fixtures_are_enforced() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(PROVENANCE_SCRIPT),
            "--fixtures-dir",
            str(FIXTURES_DIR),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "FIXTURE PASS: known-good Sigstore attested release (pass)" in result.stdout
    assert "FIXTURE PASS: missing attestation schema is rejected (fail)" in result.stdout
    assert "FIXTURE PASS: wrong workflow identity is rejected (fail)" in result.stdout
    assert "FIXTURE PASS: mismatched artifact hash is rejected (fail)" in result.stdout
    assert "FIXTURE PASS: unexpected OIDC issuer is rejected (fail)" in result.stdout
    assert "FIXTURE PASS: transparency log outage fails closed (fail)" in result.stdout
    assert "FIXTURE PASS: attestation target mismatch is rejected (fail)" in result.stdout
    assert "FIXTURE PASS: workflow rename identity drift is rejected (fail)" in result.stdout
    assert "FIXTURE PASS: trust-root rotation fails closed (fail)" in result.stdout


def test_release_attestation_builder_uses_exact_workflow_identity(tmp_path: Path) -> None:
    artifact = tmp_path / "civiccore-0.22.1-py3-none-any.whl"
    artifact.write_text("wheel bytes", encoding="utf-8")

    attestation = build_release_attestation(
        repo="CivicSuite/civiccore",
        tag_name="v0.22.1",
        tag_ref_type="commit",
        tag_ref_sha="a" * 40,
        target_commit="a" * 40,
        target_tree="b" * 40,
        workflow_run_id="25346024240",
        artifacts_dir=tmp_path,
    )

    assert attestation["schema_version"] == 1
    assert (
        attestation["build"]["workflow_identity"]
        == "https://github.com/CivicSuite/civiccore/.github/workflows/release.yml@refs/tags/v0.22.1"
    )
    assert attestation["build"]["oidc_issuer"] == "https://token.actions.githubusercontent.com"
    assert attestation["artifacts"] == [
        {
            "name": "civiccore-0.22.1-py3-none-any.whl",
            "sha256": "67c0d8f7de19e30c2d5891030a0b37cbfcdd240852b53055c0b28290ad52290b",
        }
    ]
    assert canonical_json_bytes(attestation).decode("utf-8").startswith(
        '{"artifacts":[{"name":"civiccore-0.22.1-py3-none-any.whl"'
    )
