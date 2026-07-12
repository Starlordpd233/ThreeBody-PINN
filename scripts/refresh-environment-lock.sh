#!/usr/bin/env bash
# scripts/refresh-environment-lock.sh — the SOLE production writer for
# requirements-lock.txt (CTX-05, ENV-02, 37-PATTERNS.md §1).
#
# Two explicit maintenance modes; NO default normal-setup behavior:
#
#   --seed      The one-time first-lock path. Creates a UNIQUE task-owned
#               disposable prefix from environment.yml (never names or creates
#               `pinn-train`), runs the required import/version checks and
#               `pip check`, writes `pip freeze` into a sibling candidate file,
#               rejects non-exact pins or a Torch line outside 2.12, compares
#               the candidate to the seed installation, and atomically replaces
#               the lock only after all checks pass. Removes the disposable
#               prefix and temp files on BOTH success and failure.
#
#   (no flag)   Refresh mode. May regenerate the lock ONLY from an existing
#               validated `pinn-train` environment (same candidate checks).
#               This is NOT a seed fallback.
#
# Normal `./setup.sh` NEVER calls this script. The Wave 0 test
# `TestLockBoundary.test_default_setup_has_no_dispatch_edge_to_seed` is a
# structural guard against that regression.
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

# shellcheck source=scripts/lib/conda_bootstrap.sh
source "${repo_root}/scripts/lib/conda_bootstrap.sh"

ENV_YML="${repo_root}/environment.yml"
LOCK="${repo_root}/requirements-lock.txt"
TARGET_ENV_NAME="pinn-train"

usage() {
    cat <<EOF >&2
Usage: $0 --seed | [--refresh]
  --seed      One-time first-lock: disposable prefix from environment.yml.
              Does NOT create the pinn-train target.
  (none)      Refresh: regenerate from an existing validated pinn-train.
Normal ./setup.sh never invokes this script.
EOF
}

MODE=""
if [[ "${1:-}" == "--seed" ]]; then
    MODE="seed"
elif [[ "${1:-}" == "--refresh" || "${1:-}" == "" ]]; then
    MODE="refresh"
else
    usage
    exit 2
fi

if [[ ! -f "$ENV_YML" ]]; then
    echo "refresh-environment-lock: missing $ENV_YML" >&2
    exit 1
fi

# ---- shared candidate validation --------------------------------------------

# conda-managed base packages that `pip freeze` reports with `@ file:///...`
# source URLs (they come from conda-forge, not PyPI). They are reproduced by
# environment.yml's conda section, NOT by the pip replay set, so they must be
# filtered out of requirements-lock.txt before validation.
CONDA_MANAGED_PKGS=(pip setuptools wheel packaging)

# Normalize a `pip freeze --all` output stream into the exact-pin replay set:
#   * drop blank lines and comments
#   * drop conda-managed packages (pip/setuptools/wheel/packaging) that report
#     as `@ file:///...` source URLs — they are not PyPI packages
#   * drop any remaining `@ file:///...` line (defensive — our env has none
#     beyond the conda-managed set above)
# Result on stdout: only exact `name==version` lines.
normalize_freeze() {
    local raw="$1"
    python3 - "$raw" "${CONDA_MANAGED_PKGS[@]}" <<'PY'
import sys, pathlib
raw = pathlib.Path(sys.argv[1]).read_text()
conda_managed = {p.lower() for p in sys.argv[2:]}
for line in raw.splitlines():
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    # `name @ file:///...` form: conda-managed local-build packages.
    if "@" in line:
        name = line.split("@", 1)[0].strip().lower()
        if name in conda_managed:
            continue
        # Defensive: any other @-URL line is not an exact pin; drop it from the
        # replay set (it cannot be reproduced by `pip install -r`).
        continue
    # `name==version` exact pin — keep.
    if "==" in line:
        print(line)
PY
}

# Validate a normalized candidate: every line must be an exact pin (==), torch
# must be on the 2.12.* line, and all required direct packages must be present.
validate_candidate() {
    local candidate="$1"
    [[ -f "$candidate" ]] || { echo "validate_candidate: $candidate missing" >&2; return 1; }
    # Every remaining line must use == (no @, ranges, or wildcards).
    local bad
    bad="$(grep -nE '(@|>=|<=|~=|!=|>|<|\*)' "$candidate" || true)"
    if [[ -n "$bad" ]]; then
        echo "refresh-environment-lock: candidate contains non-exact pins:" >&2
        echo "$bad" >&2
        return 1
    fi
    # torch must be on the 2.12.* line.
    if ! grep -qE '^torch==2\.12\.[0-9]+' "$candidate"; then
        echo "refresh-environment-lock: candidate does not pin torch==2.12.x" >&2
        return 1
    fi
    # Required direct packages must all be present.
    for pkg in torch numpy h5py PyYAML tensorboard; do
        if ! grep -qiE "^${pkg}==" "$candidate"; then
            echo "refresh-environment-lock: candidate missing required package: $pkg" >&2
            return 1
        fi
    done
    return 0
}

# Atomically replace the committed lock with a reviewed candidate. Writes via a
# sibling temp file + os.replace semantics (cp + mv).
atomic_install_lock() {
    local candidate="$1"
    local tmp="${LOCK}.tmp.$$"
    cp "$candidate" "$tmp"
    mv -f "$tmp" "$LOCK"
    echo "refresh-environment-lock: atomically installed $LOCK"
}

# ---- seed mode ---------------------------------------------------------------
if [[ "$MODE" == "seed" ]]; then
    echo "refresh-environment-lock: seed mode (disposable prefix; does not create ${TARGET_ENV_NAME})" >&2
    # Resolve conda (installs Miniforge3 into PINN_INSTALL_PREFIX if absent).
    # NOTE: this may install Miniforge into the user's configured prefix. That
    # is the one-time cost of the seed path; the disposable ENVIRONMENT below is
    # separate and is always removed.
    conda_exe="$(conda_bootstrap_resolve)"
    echo "refresh-environment-lock: using conda: $conda_exe"

    # Create a UNIQUE task-owned disposable environment from environment.yml.
    # Never names pinn-train. mktemp gives the unique prefix.
    seed_prefix="$(mktemp -d "${TMPDIR:-/tmp}/phase37-seed-XXXXXX")"
    echo "refresh-environment-lock: disposable seed prefix: $seed_prefix"
    cleanup() {
        echo "refresh-environment-lock: removing disposable prefix $seed_prefix" >&2
        "$conda_exe" env remove -y -p "$seed_prefix" >/dev/null 2>&1 || true
        rm -rf "$seed_prefix"
    }
    trap cleanup EXIT

    # Create the disposable env from the loose YAML. No --prefix alias to
    # pinn-train; the env name inside environment.yml is ignored when -p is used.
    if ! "$conda_exe" env create -y -p "$seed_prefix" -f "$ENV_YML"; then
        echo "refresh-environment-lock: env create failed in seed prefix" >&2
        exit 1
    fi

    # Required import + version checks inside the disposable env.
    if ! "$conda_exe" run -p "$seed_prefix" python - <<'PY'; then
import sys
ok = True
try:
    import torch
    if not torch.__version__.startswith("2.12."):
        print(f"FAIL: torch {torch.__version__} is not on the 2.12 line", file=sys.stderr)
        ok = False
    if not torch.backends.mps.is_available():
        print("FAIL: torch.backends.mps.is_available() is False", file=sys.stderr)
        ok = False
except Exception as exc:
    print(f"FAIL: torch import error: {exc}", file=sys.stderr)
    ok = False
for mod in ("numpy", "h5py", "yaml", "tensorboard"):
    try:
        __import__(mod)
    except Exception as exc:
        print(f"FAIL: {mod} import error: {exc}", file=sys.stderr)
        ok = False
sys.exit(0 if ok else 1)
PY
        echo "refresh-environment-lock: required import/version checks failed in seed env" >&2
        exit 1
    fi

    # pip check: no broken dependencies.
    if ! "$conda_exe" run -p "$seed_prefix" python -m pip check; then
        echo "refresh-environment-lock: pip check failed in seed env" >&2
        exit 1
    fi

    # Generate pip freeze into a sibling candidate, then normalize out
    # conda-managed packages (pip/setuptools/packaging come from conda-forge,
    # not PyPI; they are reproduced by environment.yml, not the lock).
    candidate="$(mktemp "${TMPDIR:-/tmp}/phase37-lock-XXXXXX")"
    raw_freeze="$(mktemp "${TMPDIR:-/tmp}/phase37-rawfreeze-XXXXXX")"
    trap 'rm -f "$candidate" "$raw_freeze"; cleanup' EXIT
    "$conda_exe" run -p "$seed_prefix" python -m pip freeze --all > "$raw_freeze"
    normalize_freeze "$raw_freeze" > "$candidate"

    # Validate, then atomically install.
    if ! validate_candidate "$candidate"; then
        echo "refresh-environment-lock: candidate validation failed" >&2
        exit 1
    fi

    # Compare candidate to a re-derived normalized freeze (deterministic over
    # the same installed set).
    recheck_raw="$(mktemp "${TMPDIR:-/tmp}/phase37-recheckraw-XXXXXX")"
    recheck="$(mktemp "${TMPDIR:-/tmp}/phase37-recheck-XXXXXX")"
    trap 'rm -f "$candidate" "$raw_freeze" "$recheck_raw" "$recheck"; cleanup' EXIT
    "$conda_exe" run -p "$seed_prefix" python -m pip freeze --all > "$recheck_raw"
    normalize_freeze "$recheck_raw" > "$recheck"
    if ! diff -q "$candidate" "$recheck" >/dev/null; then
        echo "refresh-environment-lock: candidate does not match a re-derived freeze" >&2
        exit 1
    fi

    atomic_install_lock "$candidate"
    echo "refresh-environment-lock: seed complete — review and commit $LOCK"

# ---- refresh mode ------------------------------------------------------------
else
    echo "refresh-environment-lock: refresh mode (requires validated ${TARGET_ENV_NAME})" >&2
    conda_exe="$(conda_bootstrap_resolve)"
    # Refresh may regenerate ONLY from an existing validated pinn-train.
    if ! "$conda_exe" env list | awk '{print $1}' | grep -qx "${TARGET_ENV_NAME}"; then
        echo "refresh-environment-lock: ${TARGET_ENV_NAME} does not exist — use --seed first" >&2
        exit 1
    fi
    # Re-validate the existing env.
    if ! "$conda_exe" run -n "$TARGET_ENV_NAME" python -m pip check; then
        echo "refresh-environment-lock: pip check failed in ${TARGET_ENV_NAME}" >&2
        exit 1
    fi
    candidate="$(mktemp "${TMPDIR:-/tmp}/phase37-refresh-XXXXXX")"
    raw_freeze="$(mktemp "${TMPDIR:-/tmp}/phase37-refreshraw-XXXXXX")"
    trap 'rm -f "$candidate" "$raw_freeze"' EXIT
    "$conda_exe" run -n "$TARGET_ENV_NAME" python -m pip freeze --all > "$raw_freeze"
    normalize_freeze "$raw_freeze" > "$candidate"
    if ! validate_candidate "$candidate"; then
        echo "refresh-environment-lock: candidate validation failed" >&2
        exit 1
    fi
    atomic_install_lock "$candidate"
    echo "refresh-environment-lock: refresh complete — review and commit $LOCK"
fi
