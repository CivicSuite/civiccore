"""Smoke test - proves the package is importable and version-tagged."""


def test_import_civiccore() -> None:
    import civiccore

    assert civiccore.__version__ == "0.5.0"
    assert civiccore.AuditHashChain
    assert civiccore.SourceReference
    assert civiccore.ExportManifest
    assert civiccore.ExportBundle
    assert civiccore.CityProfile
