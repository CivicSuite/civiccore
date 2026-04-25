#!/usr/bin/env bash
# civiccore/scripts/verify-release.sh - civiccore release gate.
#
# Read-only verification of civiccore's pre-push readiness. Checks:
#   1. Test suite (pytest tests/)
#   2. Lint (ruff check .)
#   3. Version lockstep between pyproject.toml and civiccore/__init__.py
#   4. Required Rule 9 doc artifacts present on disk
#   5. Build artifacts (sdist + wheel via python -m build)
#   6. Fresh virtualenv install from the built wheel, exact version check,
#      and import smoke for the migration runner
#
# Exit 0 when every check passes; exit 1 on any failure.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

PYTHON_CMD=()
if command -v python >/dev/null 2>&1; then
    PYTHON_CMD=(python)
elif command -v python.exe >/dev/null 2>&1; then
    PYTHON_CMD=(python.exe)
elif command -v py >/dev/null 2>&1; then
    PYTHON_CMD=(py -3)
elif command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD=(python3)
else
    echo "No Python interpreter found on PATH (checked python, python3, py)." >&2
    exit 1
fi

FAILED=0
pass() { printf '  \033[0;32m[PASS]\033[0m %s\n' "$*"; }
fail() { printf '  \033[0;31m[FAIL]\033[0m %s\n' "$*" >&2; FAILED=1; }
info() { printf '\n\033[1;34m%s\033[0m\n' "$*"; }

# --- 1. pytest ---------------------------------------------------------------
info "1. pytest"
if "${PYTHON_CMD[@]}" -m pytest tests/ -v --tb=short; then
    pass "test suite green"
else
    fail "pytest failed"
fi

# --- 2. ruff -----------------------------------------------------------------
info "2. ruff check"
if "${PYTHON_CMD[@]}" -m ruff check .; then
    pass "lint clean"
else
    fail "ruff reported issues"
fi

# --- 3. version lockstep (pyproject.toml <-> civiccore/__init__.py) ---------
info "3. version lockstep"
PY_VER=$(grep -oE '^version[[:space:]]*=[[:space:]]*"[^"]+"' pyproject.toml 2>/dev/null \
    | head -1 \
    | sed -E 's/^version[[:space:]]*=[[:space:]]*"([^"]+)"/\1/' || true)
INIT_VER=$(grep -oE '__version__[[:space:]]*=[[:space:]]*"[^"]+"' civiccore/__init__.py 2>/dev/null \
    | head -1 \
    | sed -E 's/.*"([^"]+)"/\1/' || true)

printf '      pyproject.toml          %s\n' "${PY_VER:-<missing>}"
printf '      civiccore/__init__.py   %s\n' "${INIT_VER:-<missing>}"

if [ -n "$PY_VER" ] && [ -n "$INIT_VER" ] && [ "$PY_VER" = "$INIT_VER" ]; then
    pass "two surfaces agree on $PY_VER"
else
    fail "version mismatch - surfaces do not agree"
fi

# --- 4. required docs --------------------------------------------------------
info "4. required docs present"
for f in README.md CHANGELOG.md CONTRIBUTING.md LICENSE .gitignore docs/index.html; do
    if [ -f "$f" ]; then
        pass "$f"
    else
        fail "missing: $f"
    fi
done

# --- 5. build artifacts ------------------------------------------------------
info "5. build artifacts"
rm -rf dist/ build/
if "${PYTHON_CMD[@]}" -m build; then
    pass "python -m build succeeded"
else
    fail "python -m build failed"
fi

# --- 6. wheel install in a clean virtualenv ---------------------------------
info "6. clean virtualenv wheel install"
if "${PYTHON_CMD[@]}" - <<'PY'
from __future__ import annotations

import glob
import os
import shutil
import subprocess
import sys
import tempfile
import venv
from pathlib import Path


def main() -> int:
    wheels = sorted(glob.glob("dist/civiccore-*.whl"))
    if not wheels:
        print("missing built wheel in dist/", file=sys.stderr)
        return 1

    wheel_path = Path(wheels[0]).resolve()
    temp_dir = Path(tempfile.mkdtemp(prefix="civiccore-release-"))

    try:
        builder = venv.EnvBuilder(with_pip=True)
        builder.create(temp_dir)

        candidates = [
            temp_dir / "Scripts" / "python.exe",
            temp_dir / "Scripts" / "python",
            temp_dir / "bin" / "python",
        ]
        venv_python = next((path for path in candidates if path.exists()), None)
        if venv_python is None:
            print("could not locate virtualenv python executable", file=sys.stderr)
            return 1

        subprocess.run(
            [str(venv_python), "-m", "pip", "install", "--upgrade", "pip", str(wheel_path)],
            check=True,
        )
        subprocess.run(
            [
                str(venv_python),
                "-c",
                (
                    "from importlib.metadata import version; "
                    "import civiccore; "
                    "from civiccore.migrations.runner import upgrade_to_head; "
                    "assert version('civiccore') == '0.2.0'; "
                    "assert civiccore.__version__ == '0.2.0'; "
                    "assert callable(upgrade_to_head); "
                    "print('fresh-venv import smoke OK')"
                ),
            ],
            check=True,
        )
        print(f"fresh virtualenv install verified via {venv_python}")
        return 0
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


raise SystemExit(main())
PY
then
    pass "fresh virtualenv import + exact version verification succeeded"
else
    fail "fresh virtualenv import/version verification failed"
fi

# --- summary -----------------------------------------------------------------
echo ""
if [ "$FAILED" -eq 0 ]; then
    printf '\033[0;32mVERIFY-RELEASE: PASSED\033[0m\n'
    exit 0
else
    printf '\033[0;31mVERIFY-RELEASE: FAILED\033[0m\n'
    exit 1
fi
