from pathlib import Path

import yaml


def test_github_workflow_yaml_files_parse() -> None:
    workflow_dir = Path(".github/workflows")
    workflows = sorted(workflow_dir.glob("*.yml"))

    assert workflows
    for workflow in workflows:
        data = yaml.safe_load(workflow.read_text(encoding="utf-8"))
        assert isinstance(data, dict), workflow
        assert data.get("name"), workflow
        assert data.get("jobs"), workflow


def test_release_workflow_uploads_explicit_downloaded_asset_files() -> None:
    workflow = yaml.safe_load(
        Path(".github/workflows/release.yml").read_text(encoding="utf-8")
    )
    release_steps = workflow["jobs"]["release"]["steps"]
    download_step = release_steps[0]
    create_release_script = release_steps[1]["run"]

    assert download_step["uses"] == "actions/download-artifact@v8"
    assert download_step["with"]["name"] == "civiccore-dist"
    assert download_step["with"]["path"] == "release-assets/"
    assert "release-assets/dist/*" in create_release_script
    assert "release-assets/release-attestation.json \\" in create_release_script
    assert "release-assets/release-attestation.json.bundle \\" in create_release_script
    assert "release-assets/*" not in create_release_script
