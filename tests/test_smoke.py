"""Smoke test — proves the package is importable and version-tagged.

Phase 0 has no functional behavior to test. The only contract at this
stage is `import civiccore` succeeds and exposes a PEP 440 dev version.
"""


def test_import_civiccore() -> None:
    import civiccore

    assert civiccore.__version__.startswith("0.1.")
