#!/usr/bin/env bash
# civiccore/scripts/verify-release.sh — Phase 1 release gate.
#
# Read-only verification of civiccore's pre-push readiness. Checks:
#   1. Test suite (pytest tests/)
#   2. Lint (ruff check .)
#   3. Version lockstep between pyproject.toml and civiccore/__init__.py
#   4. Required Rule 9 doc artifacts present on disk
#
# Exit 0 when every check passes; exit 1 on any failure. Never writes.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

FAILED=0
pass() { printf '  \033[0;32m[PASS]\033[0m %s\n' "$*"; }
fail() { printf '  \033[0;31m[FAIL]\033[0m %s\n' "$*" >&2; FAILED=1; }
info() { printf '\n\033[1;34m%s\033[0m\n' "$*"; }

# --- 1. pytest ---------------------------------------------------------------
info "1. pytest"
if python -m pytest tests/ -v --tb=short; then
    pass "test suite green"
else
    fail "pytest failed"
fi

# --- 2. ruff -----------------------------------------------------------------
info "2. ruff check"
if python -m ruff check .; then
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
    fail "version mismatch — surfaces do not agree"
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

# --- summary -----------------------------------------------------------------
echo ""
if [ "$FAILED" -eq 0 ]; then
    printf '\033[0;32mVERIFY-RELEASE: PASSED\033[0m\n'
    exit 0
else
    printf '\033[0;31mVERIFY-RELEASE: FAILED\033[0m\n'
    exit 1
fi
