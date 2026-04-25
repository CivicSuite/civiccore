"""Smoke test - proves the package is importable and version-tagged.

Phase 0 has no functional behavior to test. The only contract at this
stage is `import civiccore` succeeds and exposes the exact release version.
"""


def test_import_civiccore() -> None:
    import civiccore

    assert civiccore.__version__ == "0.2.0"
