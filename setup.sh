#!/usr/bin/env bash
# setup.sh — Phase 37 / ENV-01 / ENV-02 fresh-Mac one-command bootstrap.
#
# Contract (CTX-01..CTX-05, 37-PATTERNS.md §1):
#   * Root-level entry: no Make, Python, or pre-existing conda prerequisite.
#   * Obtains compatible arm64 Miniforge via the shared bootstrap library
#     (installs only if absent; never replaces an existing conda silently).
#   * Default command REQUIRES both committed inputs (environment.yml +
#     requirements-lock.txt). If either is absent, exits before target
#     creation with explicit remediation. NEVER invokes the refresh script
#     or its seed mode — that is a separate maintenance operation.
#   * From an absent `pinn-train`: creates it from the committed YAML and
#     replays the exact lock. From a present `pinn-train`: validation only.
#     NEVER runs a solver/update on rerun, recreates drift silently, replaces
#     a prefix, alters shell startup files, or claims to activate the caller.
#   * Invokes the verifier through `conda run -n pinn-train` and prints
#     exactly `source <base>/etc/profile.d/conda.sh && conda activate pinn-train`.
set -euo pipefail

# Resolve repository root from this script's own location (works from any CWD;
# does not require git, Make, or Python).
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$script_dir"
cd "$repo_root"

# shellcheck source=scripts/lib/conda_bootstrap.sh
source "${repo_root}/scripts/lib/conda_bootstrap.sh"

ENV_YML="${repo_root}/environment.yml"
LOCK="${repo_root}/requirements-lock.txt"
TARGET_ENV_NAME="pinn-train"
VERIFY_PY="${repo_root}/scripts/verify_environment.py"
EVIDENCE_ROOT="${repo_root}/.planning/phases/37-developer-environment-precision-adjudication/evidence/environment"

die() { echo "setup.sh: $*" >&2; exit 1; }

# ---- gate 1: committed inputs must exist BEFORE any target mutation -------
if [[ ! -f "$ENV_YML" ]]; then
    die "missing ${ENV_YML} — this setup requires the committed environment pair. Run 'scripts/refresh-environment-lock.sh --seed' (one-time maintenance) to generate the pair first."
fi
if [[ ! -f "$LOCK" ]]; then
    die "missing ${LOCK} — ordinary setup does not create the lock. Run 'scripts/refresh-environment-lock.sh --seed' (one-time maintenance), review the candidate, and commit it before running setup."
fi

# ---- gate 2: compatible conda (installs Miniforge3 if absent) -------------
conda_exe="$(conda_bootstrap_resolve)"
echo "setup.sh: using conda: $conda_exe"

# ---- determine target state ----------------------------------------------
# Does the named environment already exist?
env_exists() {
    "$conda_exe" env list 2>/dev/null | awk '{print $1}' | grep -qx "$1"
}

if env_exists "$TARGET_ENV_NAME"; then
    # ---- validation-only rerun (CTX-03: second run is a no-op pass) ------
    echo "setup.sh: ${TARGET_ENV_NAME} exists — validating only (no solver, no update)"
else
    # ---- first-time creation from the committed pair ---------------------
    echo "setup.sh: creating ${TARGET_ENV_NAME} from the committed pair"
    # Create from the loose YAML, then replay the exact lock on top. This
    # two-step ensures the env's pip set matches the lock byte-for-byte.
    "$conda_exe" env create -y -n "$TARGET_ENV_NAME" -f "$ENV_YML"
    # Replay the exact lock to guarantee installed == committed.
    "$conda_exe" run -n "$TARGET_ENV_NAME" python -m pip install --no-deps -r "$LOCK"
    # Re-verify no broken deps after the replay.
    "$conda_exe" run -n "$TARGET_ENV_NAME" python -m pip check
fi

# ---- gate 3: verify the runtime contract and emit a fingerprint -----------
# The verifier runs inside pinn-train via `conda run`. It writes a new
# timestamped fingerprint pair under EVIDENCE_ROOT (exclusive, non-overwrite).
# --check-only is the no-write validation path; the normal path here adds the
# fingerprint.
FINGERPRINT_JSON=""
FINGERPRINT_MARKDOWN=""
# Capture the emitted paths from the verifier's stdout (it prints them).
verify_output="$("$conda_exe" run -n "$TARGET_ENV_NAME" python "$VERIFY_PY" \
    --lock-file "$LOCK" --output-root "$EVIDENCE_ROOT" 2>&1)" || {
    echo "$verify_output" >&2
    die "environment verification failed — see above; no fingerprint written"
}
echo "$verify_output"
# Parse FINGERPRINT_JSON / FINGERPRINT_MARKDOWN from the verifier's stdout.
FINGERPRINT_JSON="$(printf '%s\n' "$verify_output" | sed -n 's/^FINGERPRINT_JSON=//p' || true)"
FINGERPRINT_MARKDOWN="$(printf '%s\n' "$verify_output" | sed -n 's/^FINGERPRINT_MARKDOWN=//p' || true)"
if [[ -z "$FINGERPRINT_JSON" || -z "$FINGERPRINT_MARKDOWN" ]]; then
    die "verifier did not emit FINGERPRINT_JSON / FINGERPRINT_MARKDOWN paths"
fi

echo
echo "setup.sh: done."
echo "FINGERPRINT_JSON=$FINGERPRINT_JSON"
echo "FINGERPRINT_MARKDOWN=$FINGERPRINT_MARKDOWN"
echo
echo "To activate ${TARGET_ENV_NAME} in your own shell, run:"
conda_bootstrap_print_activation
