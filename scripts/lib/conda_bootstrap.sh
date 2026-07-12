#!/usr/bin/env bash
# scripts/lib/conda_bootstrap.sh — shared Phase 37 conda/Miniforge bootstrap.
#
# Source this file; do not execute it directly. It exports one function,
# `conda_bootstrap_resolve`, used by both `setup.sh` (normal path) and
# `scripts/refresh-environment-lock.sh --seed` (the one-time first-lock path).
#
# Contract (CTX-01..CTX-05, 37-PATTERNS.md §1, 37-RESEARCH.md "bootstrap"):
#   * Reject non-Darwin or non-arm64 BEFORE any network access.
#   * Discover a compatible conda in this order, accepting the first that passes
#     executable + root-prefix + osx-arm64 platform checks:
#       1. PINN_CONDA_EXE   (caller-supplied override)
#       2. PINN_INSTALL_PREFIX/bin/conda (configured Miniforge prefix)
#       3. "${HOME}/miniforge3/bin/conda" (conventional Miniforge3 location)
#       4. `command -v conda` (PATH; only if it points at Miniforge/Miniconda,
#          never Anaconda)
#   * If no compatible conda is found AND the configured prefix is empty,
#     download a pinned, named Miniforge3-MacOSX-arm64 release, verify its
#     committed SHA-256, and batch-install it (`bash installer -b -p PREFIX`).
#   * NEVER: pipe a download into a shell; overwrite an occupied prefix; call
#     `conda init`; edit shell startup files; use a moving `releases/latest` URL;
#     invoke a system Python runtime.
#
# The caller must `set -euo pipefail` before sourcing.
#
# Environment variables consumed:
#   PINN_INSTALL_PREFIX  — where Miniforge3 lives / should be installed.
#                          Default: "${HOME}/miniforge3".
#   PINN_CONDA_EXE       — explicit conda executable override (optional).

# Pinned, named, immutable Miniforge3 release (37-RESEARCH.md Pitfall 3: do NOT
# use releases/latest — a moving URL undermines replay and supply-chain review).
# Verified from the signed GitHub release page on 2026-07-12.
MINIFORGE_VERSION="26.3.2-3"
MINIFORGE_INSTALLER_NAME="Miniforge3-${MINIFORGE_VERSION}-MacOSX-arm64.sh"
MINIFORGE_URL="https://github.com/conda-forge/miniforge/releases/download/${MINIFORGE_VERSION}/${MINIFORGE_INSTALLER_NAME}"
MINIFORGE_SHA256="59168f1e24d0a4ad9932021170809fca836cd240e183eeeb331d5bcfc0098168"

conda_bootstrap_die() {
    echo "conda_bootstrap: $*" >&2
    exit 1
}

# Verify the host is Darwin/arm64 before any download. Returns 0 if compatible.
conda_bootstrap_assert_host() {
    local os arch
    os="$(uname -s)"
    arch="$(uname -m)"
    if [[ "$os" != "Darwin" ]]; then
        conda_bootstrap_die "unsupported OS '$os' — Phase 37 bootstrap requires macOS (Darwin)"
    fi
    if [[ "$arch" != "arm64" ]]; then
        conda_bootstrap_die "unsupported architecture '$arch' — Phase 37 bootstrap requires Apple silicon (arm64)"
    fi
}

# Check whether a candidate conda executable is compatible: exists, is
# executable, reports a root prefix, and is osx-arm64. Prints nothing; returns 0
# if compatible, non-zero otherwise.
_conda_bootstrap_candidate_ok() {
    local candidate="$1"
    [[ -n "$candidate" ]] || return 1
    [[ -x "$candidate" ]] || return 1
    # Must not be Anaconda (Anaconda's default channels conflict with the
    # conda-forge-only contract).
    local resolved
    resolved="$(readlink -f "$candidate" 2>/dev/null || echo "$candidate")"
    case "$resolved" in
        *anaconda*|*Anaconda*) return 1 ;;
    esac
    # Must report an osx-arm64 platform.
    local platform
    platform="$("$candidate" info --json 2>/dev/null \
        | python3 -c 'import json,sys; print(json.load(sys.stdin).get("platform",""))' 2>/dev/null || true)"
    [[ "$platform" == "osx-arm64" ]] || return 1
    return 0
}

# Download the pinned installer into a mktemp -d directory and verify its
# committed SHA-256. Prints the installer path on stdout. The caller owns
# cleanup of the temp directory (the installer must persist across function
# boundaries, so this helper does NOT install a RETURN trap).
_conda_bootstrap_download() {
    local tmp_dir installer
    tmp_dir="$(mktemp -d)"
    installer="${tmp_dir}/${MINIFORGE_INSTALLER_NAME}"
    echo "conda_bootstrap: downloading ${MINIFORGE_INSTALLER_NAME}" >&2
    # -f fail on HTTP error, -L follow redirects, -o write to file. NEVER pipe
    # to shell.
    if ! curl -fL --retry 3 -o "$installer" "$MINIFORGE_URL"; then
        rm -rf "$tmp_dir"
        conda_bootstrap_die "download failed: $MINIFORGE_URL"
    fi
    echo "conda_bootstrap: verifying SHA-256" >&2
    local actual_sha
    actual_sha="$(shasum -a 256 "$installer" | awk '{print $1}')"
    if [[ "$actual_sha" != "$MINIFORGE_SHA256" ]]; then
        rm -rf "$tmp_dir"
        conda_bootstrap_die "SHA-256 mismatch for ${MINIFORGE_INSTALLER_NAME}: expected ${MINIFORGE_SHA256}, got ${actual_sha}"
    fi
    echo "$installer"
}

# Install Miniforge3 into an EMPTY configurable prefix via batch mode. Refuses
# if the prefix exists and is non-empty (would otherwise overwrite an occupied
# prefix — 37-PATTERNS.md: "never invoke the installer's update/overwrite").
_conda_bootstrap_install() {
    local prefix="$1"
    [[ -n "$prefix" ]] || conda_bootstrap_die "install prefix is empty"
    if [[ -e "$prefix" ]]; then
        if [[ -n "$(ls -A "$prefix" 2>/dev/null)" ]]; then
            conda_bootstrap_die "install prefix '$prefix' exists and is non-empty — refusing to overwrite"
        fi
        # The Miniforge batch installer (`-b -p`) refuses to install into an
        # existing directory and does not offer a non-overwrite flag. An empty
        # existing directory is safe to remove; remove it so the installer can
        # create the prefix itself.
        rmdir "$prefix" 2>/dev/null || true
    fi
    # Do NOT pre-create the prefix with mkdir -p: the Miniforge installer wants
    # the path absent (or use -u to update; we never update). It creates the
    # prefix itself.
    local installer tmp_dir
    installer="$(_conda_bootstrap_download)"
    # tmp_dir is the installer's parent; clean it up on exit (success or
    # failure). The installer file itself is read by `bash` and can be removed
    # once the batch install returns.
    tmp_dir="$(dirname "$installer")"
    echo "conda_bootstrap: batch-installing into $prefix" >&2
    # -b batch, -p prefix. Non-interactive install does NOT call conda init or
    # touch shell startup files (Miniforge docs).
    if ! bash "$installer" -b -p "$prefix"; then
        rm -rf "$tmp_dir"
        conda_bootstrap_die "batch install failed into '$prefix'"
    fi
    rm -rf "$tmp_dir"
    echo "${prefix}/bin/conda"
}

# Resolve a compatible conda executable, installing Miniforge3 if needed.
# Prints the conda executable path on stdout. Caller sets PINN_INSTALL_PREFIX
# before calling (defaults to ${HOME}/miniforge3).
conda_bootstrap_resolve() {
    conda_bootstrap_assert_host
    local prefix="${PINN_INSTALL_PREFIX:-${HOME}/miniforge3}"
    # 1. Caller override.
    if [[ -n "${PINN_CONDA_EXE:-}" ]]; then
        if _conda_bootstrap_candidate_ok "$PINN_CONDA_EXE"; then
            echo "$PINN_CONDA_EXE"
            return 0
        fi
        conda_bootstrap_die "PINN_CONDA_EXE='$PINN_CONDA_EXE' is not a compatible osx-arm64 conda"
    fi
    # 2. Configured prefix.
    local prefix_conda="${prefix}/bin/conda"
    if _conda_bootstrap_candidate_ok "$prefix_conda"; then
        echo "$prefix_conda"
        return 0
    fi
    # 3. Conventional Miniforge3 location.
    local home_conda="${HOME}/miniforge3/bin/conda"
    if [[ "$home_conda" != "$prefix_conda" ]] && _conda_bootstrap_candidate_ok "$home_conda"; then
        echo "$home_conda"
        return 0
    fi
    # 4. PATH (only Miniforge/Miniconda, never Anaconda).
    local path_conda
    path_conda="$(command -v conda 2>/dev/null || true)"
    if [[ -n "$path_conda" ]] && _conda_bootstrap_candidate_ok "$path_conda"; then
        echo "$path_conda"
        return 0
    fi
    # No compatible conda found — install into the configured prefix. The prefix
    # must be empty (or non-existent) for a clean install.
    if [[ -e "$prefix" ]] && [[ -n "$(ls -A "$prefix" 2>/dev/null)" ]]; then
        # A non-empty prefix that is NOT a compatible conda is a hard failure,
        # not an overwrite opportunity.
        conda_bootstrap_die "prefix '$prefix' is occupied but does not contain a compatible osx-arm64 conda — refusing to install; set PINN_INSTALL_PREFIX to an empty prefix or remove the foreign content manually"
    fi
    _conda_bootstrap_install "$prefix"
}

# Print the activation instruction exactly (CTX-03). setup.sh calls this after
# a successful run; it does NOT activate the caller's shell.
conda_bootstrap_print_activation() {
    local prefix="${PINN_INSTALL_PREFIX:-${HOME}/miniforge3}"
    echo "source ${prefix}/etc/profile.d/conda.sh && conda activate pinn-train"
}
