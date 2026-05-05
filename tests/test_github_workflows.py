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
