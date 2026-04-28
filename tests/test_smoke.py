"""Smoke test - proves the package is importable and version-tagged.

The package root must import cleanly, expose the exact release version, and
surface the v0.3.0 primitives needed by downstream modules.
"""


def test_import_civiccore() -> None:
    import civiccore

    assert civiccore.__version__ == "0.3.0"
    assert civiccore.AuditHashChain
    assert civiccore.SourceReference
    assert civiccore.ExportManifest
    assert civiccore.ExportBundle
    assert civiccore.CityProfile
