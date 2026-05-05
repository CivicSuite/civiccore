from __future__ import annotations

import json
import shutil
import subprocess
from hashlib import sha256
from pathlib import Path

import pytest


PACK = Path("docs/evidence/co8-civiccore-procurement-evidence-pack")


REQUIRED_FILES = {
    "README-install-verify-worked-example.md",
    "claims-registry.md",
    "evidence-pack-manifest.json",
    "incident-response-runbook.md",
    "index.md",
    "license-manifest.json",
    "license-manifest.md",
    "patch-cadence.md",
    "preflight.md",
    "sbom-civiccore-m1-freeze-pip-inspect.json",
    "sbom-v0.22.1-pip-inspect.json",
    "sbom-v1.0-rc-main-3c4c34c-pip-inspect.json",
    "sovereignty-proof.md",
    "threat-model-signature.allowed_signers",
    "threat-model-signing-public.pem",
    "threat-model.md",
    "threat-model.md.sha256",
    "threat-model.md.sig",
}


def test_co8_procurement_pack_required_files_exist() -> None:
    missing = sorted(name for name in REQUIRED_FILES if not (PACK / name).is_file())
    assert not missing


def test_co8_procurement_pack_manifest_hashes_match() -> None:
    manifest = json.loads((PACK / "evidence-pack-manifest.json").read_text(encoding="utf-8-sig"))
    manifest_files = {entry["path"]: entry for entry in manifest["files"]}

    expected_manifest_entries = REQUIRED_FILES - {"evidence-pack-manifest.json"}
    assert set(manifest_files) == expected_manifest_entries
    assert manifest["sprint_id"] == "CO-8"
    assert manifest["freeze_tag"] == "civiccore-m1-freeze"
    assert manifest["target_commit"] == "3c4c34ccd153eeae705a57139f6713c356328b6d"

    for name, entry in manifest_files.items():
        data = (PACK / name).read_bytes()
        assert entry["bytes"] == len(data), name
        assert entry["sha256"] == sha256(data).hexdigest(), name


def test_co8_threat_model_hash_and_signature_verify() -> None:
    threat_model = PACK / "threat-model.md"
    expected_hash = (PACK / "threat-model.md.sha256").read_text(encoding="ascii").split()[0]
    assert sha256(threat_model.read_bytes()).hexdigest() == expected_hash

    ssh_keygen = shutil.which("ssh-keygen")
    if ssh_keygen is None:
        pytest.skip("ssh-keygen is not available in this environment")

    result = subprocess.run(
        [
            ssh_keygen,
            "-Y",
            "verify",
            "-f",
            str(PACK / "threat-model-signature.allowed_signers"),
            "-I",
            "co8-civiccore-threat-model",
            "-n",
            "file",
            "-s",
            str(PACK / "threat-model.md.sig"),
        ],
        input=threat_model.read_bytes(),
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")


@pytest.mark.parametrize(
    "filename",
    [
        "sbom-v0.22.1-pip-inspect.json",
        "sbom-civiccore-m1-freeze-pip-inspect.json",
        "sbom-v1.0-rc-main-3c4c34c-pip-inspect.json",
    ],
)
def test_co8_sboms_are_valid_and_include_civiccore(filename: str) -> None:
    sbom = json.loads((PACK / filename).read_text(encoding="utf-8-sig"))
    installed = sbom["installed"]
    assert len(installed) >= 80
    civiccore = [
        item
        for item in installed
        if item.get("metadata", {}).get("name", "").lower() == "civiccore"
    ]
    assert len(civiccore) == 1
    assert civiccore[0]["metadata"]["version"] == "0.22.1"


def test_co8_license_manifest_matches_freeze_sbom_packages() -> None:
    license_manifest = json.loads((PACK / "license-manifest.json").read_text(encoding="utf-8"))
    freeze_sbom = json.loads(
        (PACK / "sbom-civiccore-m1-freeze-pip-inspect.json").read_text(encoding="utf-8-sig")
    )

    manifest_names = {pkg["name"].lower() for pkg in license_manifest["packages"]}
    freeze_names = {item["metadata"]["name"].lower() for item in freeze_sbom["installed"]}

    assert manifest_names == freeze_names
    assert "civiccore" in manifest_names
