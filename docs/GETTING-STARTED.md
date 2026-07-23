<!-- generated-by: gsd-doc-writer -->
# Getting Started

This page is the shortest path from a fresh checkout of the repository to a working Brutus build, a working Python pipeline, and a restored `simulation_data/` dataset. It is intentionally brief — it points to the canonical runbooks for full detail.

If you are opening this repository as part of a workstation migration, the canonical restore path is `docs/runbooks/migration/exact-state-mac-migration.md`. That runbook preserves `.git/`, `.venv/`, dirty tracked files, untracked files, and active hooks in a single encrypted archive; the four bulky gitignored simulation payload directories are excluded and copied manually after restore.

## Prerequisites

| Tool | Version | Used by | Notes |
|---|---|---|---|
| Python | 3.12 (the repo `.venv` is Python 3.12) | Pipeline scripts, `.venv` | Required by the restored venv; see `docs/runbooks/migration/exact-state-mac-migration.md` Phase B5. |
| `g++` | C++11 compliant | Brutus C++ build | Provided by Xcode Command Line Tools (`xcode-select --install`) on macOS. |
| `make` | any | Brutus C++ build | macOS: included with the Xcode Command Line Tools. |
| GMP (libgmp, libgmpxx) | Homebrew `gmp` | Brutus C++ build | Required for arbitrary-precision integer and rational arithmetic. |
| MPFR (libmpfr) | Homebrew `mpfr` | Brutus C++ build | Required for arbitrary-precision floating-point arithmetic. |
| `mpreal` C++ headers | at `~/src/mpreal` | Brutus C++ build | Hard-coded path in `brutus_Newton-main/makefile` (`MPRLIB = $(HOME_DIR)/src/mpreal`). Edit the makefile on hosts where this path does not exist. |
| Homebrew | current | GMP, MPFR, and the build toolchain | Standard M2 Mac install. `BREW_PREFIX = /opt/homebrew` is hard-coded in the Brutus `makefile`. |
| `git-lfs` | current | Large files in the repo | Smoke-checked by the migration runbook Phase B6. |

Python runtime libraries are pre-installed in the repo's `.venv` (a tracked-ignored local directory). The migration runbook restores `.venv` byte-for-byte; on a fresh clone without the archive, install dependencies from the README quickstart command (`pip install numpy pandas scipy h5py torch`).

## Installation steps

The fastest path is to follow the migration runbook. It restores the repo at the canonical absolute path `<home>/Desktop/3_body_problem` with the preserved `.venv` and active hooks.

1. **Read the migration runbook** — `docs/runbooks/migration/exact-state-mac-migration.md`. Phases A1–A8 run on the source Mac; Phases B1–B8 run on the new Mac. Several steps are interactive (`age -p` reads the passphrase from `/dev/tty`, `gh auth login`, Homebrew installs).
2. **Restore the encrypted archive** (B1–B3) — install `zstd`, `gh`, `age`, `git-lfs` via Homebrew, confirm Python 3.12, authenticate `gh`, then `gh release download`, verify `SHA256SUMS`, decrypt with `age`, decompress with `zstd`, and extract into the destination parent directory. The runbook refuses to merge into a populated destination; ensure the target path does not exist.
3. **Verify exact-state parity** (B4) — decrypt `MANIFEST.txt.age`, decrypt `manifest.sh.age`, regenerate the manifest on the new Mac, and `diff` against the OLD Mac baseline. The expected output is `PARITY OK - exact repo state restored except excluded simulation payloads`. Then run `git fsck --full --no-dangling` to verify object integrity.
4. **Smoke-test or repair the restored `.venv`** (B5) — run `./.venv/bin/python -c "import sys; print(sys.executable); print(sys.version)"`. If it fails, decrypt `requirements-oldmac.txt.age` and rebuild with `python3.12 -m venv .venv` followed by `pip install -r requirements-oldmac.txt`. This is an intentional host repair; `.venv` is gitignored, so `git status` does not change.
5. **Restore the four gitignored simulation payloads manually** (B8) — copy `simulation_data/Data/brutus_output/`, `simulation_data/Data/metrics/`, `simulation_data/Data/ic_final/`, and `simulation_data/Validation/prescreening/prescreening_data/` by external drive, AirDrop, `rsync`, or another non-Git method. These are excluded from the encrypted archive by design and must arrive separately.

If you are working from a fresh `git clone` (no migration archive), the runbook does not apply. In that case:

1. Clone the repository and `cd` into the project root.
2. Create a Python 3.12 virtualenv and install runtime dependencies: `pip install numpy pandas scipy h5py torch`. The README quickstart uses `python3` explicitly.
3. Export the `IC_RAW_DIR` environment variable pointing at the directory holding the raw pre-prescreening ICs. The expected subdirectories are `ic_hierarchical/` and `ic_standard_quasi_random/`. The pipeline fails at startup if this variable is unset.
4. Build Brutus (see "Build Brutus" below).
5. Restore the dataset payloads (see "Restore the dataset" below).

## Build Brutus

The Brutus C++ integrator lives in `brutus_Newton-main/` and is built from the bundled `makefile`. The `makefile` is hard-wired to an M2 Mac with Homebrew and to `<home>/src/mpreal`; for any other host, edit `BREW_PREFIX`, `HOME_DIR`, and `MPRLIB` in the file before building.

```bash
cd brutus_Newton-main
make clean
make
```

Verify the build by inspecting the output binary and running a single IC:

```bash
ls brutus                                # the compiled binary
./brutus 1e-15 130 0 10 0.08 3 /abs/path/to/ic.txt
```

The expected argument order is `<tolerance> <word_length> <t_begin> <t_end> <dt_out> <n_particles> <input_ic>`. Output is written to stdout — redirect to a file. The pipeline scripts fix `t_begin=0`, `t_end=10`, `n_particles=3` across all four dataset variants.

## Restore the dataset

The four bulky simulation payload directories are gitignored and are not part of the repository on disk:

- `simulation_data/Data/brutus_output/` (~4.7 GB)
- `simulation_data/Data/metrics/` (~1.4 GB)
- `simulation_data/Data/ic_final/` (~30 MB)
- `simulation_data/Validation/prescreening/prescreening_data/` (~11 MB)

The migration runbook excludes these by design. They must be restored separately after the encrypted archive is in place. The typical pattern is:

1. Copy the four directories to their canonical paths under the repo root (above) by external drive, AirDrop, or `rsync`.
2. Confirm `git status --short` is unchanged — these directories are gitignored, so they must not appear in the status output.
3. Spot-check a single Brutus output file with the parsing rules in `.claude/rules/dataset-reference.md`: final timestamp must be `>= 9.5`; the `Result:` footer is optional; body lines may carry 30-40 significant digits of precision.

## First run

A complete first run executes the four-stage Python pipeline against the restored dataset. The stages are independent and can be run individually; each writes into the directory expected by the next stage.

```bash
cd "$REPO_ROOT"
export IC_RAW_DIR=/path/to/ic_raw

# Stage 1: IC generation (writes into $IC_RAW_DIR/ic_hierarchical/ or $IC_RAW_DIR/ic_standard_quasi_random/)
python3 simulation_data/Scripts/ic_generation/generate_ics.py

# Stage 2: prescreening (filters unstable ICs; copies passed ICs to simulation_data/Data/ic_final/ and writes processing-index JSON under simulation_data/Validation/prescreening/)
python3 simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py

# Stage 3: Brutus integration via the compiled binary
python3 simulation_data/Scripts/brutus_runners/run_brutus_both_type_simple.py

# Hierarchical gold-standard subset (separate parameter set)
python3 simulation_data/Scripts/brutus_runners/run_brutus_hierarchical_only_mac_gold_standard.py

# Stage 4: metrics (energy / momentum / collision flags as JSON)
python3 simulation_data/Scripts/metrics_calculation/calculate_metrics.py
```

`run_brutus_both_type_simple.py` exposes `HIERARCHICAL_ICS_PER_RUN=10` and `STANDARD_ICS_PER_RUN=0` by default and enforces a 3000-second per-simulation timeout. The gold-standard hierarchical runner exposes `ICS_PER_RUN=1000`. The `brutus_standard_quasi_random_gold_standard/` outputs (under `Data/brutus_output/`) were generated partly from prior pipeline versions and have no in-repo runner that natively reproduces them.

The README §"Script Status Matrix" notes that the legacy `pinn/data-processing-pipeline-full.py` monofile (Stage 5) is import-broken in its current form: it needs the repo root added to `sys.path` before importing. (Its hyphenated filename is not a valid Python module name, so `python3 -m pinn.data-processing-pipeline-full` does **not** work.) The `simulation_data/Validation/dataset_readiness_checks/` validation scripts are marked **unverified**: their old `ValidationConfig` NameError etiology is stale (the class is defined and imported in the package sources). Rely on the Stage 4 metrics scripts (`calculate_metrics.py` / `calculate_brutus_metrics.py`) meanwhile.

## Common setup issues

These are the issues that bite a fresh setup most often. The first three are the ones the migration runbook explicitly guards against.

| Symptom | Cause | Fix |
|---|---|---|
| `age -d` reads from `/dev/tty` and hangs in a non-interactive shell | The `age -p` pipeline requires a TTY | Run the decrypt in an interactive terminal, or use the OpenSSL alternative in Appendix B of the migration runbook (verify `openssl version` reports `OpenSSL`, not `LibreSSL`). |
| `gh release download` returns 404 | The release is private and `gh` is not authenticated, or the release tag is misspelled | Run `gh auth status || gh auth login` and confirm access to `Starlordpd233/ThreeBodyProblem`. Verify `TAG` matches the date used on the source Mac. |
| `diff $WORK/MANIFEST.txt $WORK/MANIFEST_new.txt` shows non-empty output | The destination path differs from `<home>/Desktop/3_body_problem`, or `.venv` is missing, or hooks are stale | Run B5 Step 1 to smoke-test the venv; B5 Step 2 to rebuild the venv from `requirements-oldmac.txt`; B5 Step 3 to repair `core.hooksPath` and hook executability. The runbook marks these as intentional host repairs. |
| `git fsck --full --no-dangling` reports errors | Archive corruption during transfer or extraction | Re-download from the release, verify `SHA256SUMS`, re-run B3. |
| `make` fails with `lgmpxx not found` or `lmpfr not found` | GMP / MPFR are not installed, or `BREW_PREFIX` is wrong | `brew install gmp mpfr`; on a non-M2 Mac, edit `BREW_PREFIX` in `brutus_Newton-main/makefile` (the current default is `/opt/homebrew`). |
| `make` fails with `mpreal.h: No such file` | `mpreal` headers are not at the hard-coded path | Clone or copy the `mpreal` library to `~/src/mpreal`, or edit `MPRLIB` in the `makefile`. |
| `IC_RAW_DIR` not set | Required env var for Stage 1 and Stage 2 scripts | `export IC_RAW_DIR=/path/to/ic_raw` with subdirs `ic_hierarchical/` and `ic_standard_quasi_random/`. The script raises `RuntimeError` at startup if this is missing. |
| Brutus runner reports "executable not found" | `brutus_Newton-main/brutus` was not built, or the runner is invoked from a different working directory | Run `make clean && make` in `brutus_Newton-main/` before invoking the runner. |
| Final Brutus timestamp `< 9.5` | The simulation timed out or failed to converge | Increase `TIMEOUT_SECONDS` (default 3000), check `simulation_data/Documentation/problematic_ics_blacklist.json` (gitignored; present only after restore), and treat the file as scientifically invalid even if the return code was zero. Do not rely on the optional `Result:` footer. |
| `pinn/data-processing-pipeline-full.py` import errors | Internal `from core...` / `from processing...` cross-references fail under the default invocation | Add the repo root to `sys.path` before importing (the hyphenated filename is not a valid Python module, so `python3 -m pinn.data-processing-pipeline-full` does not work). |
| Hierarchical COM drift | Hierarchical ICs enforce `~0` total momentum then perturb with `sigma=0.01` noise, so COM drifts slightly | Re-center manually before translationally-invariant training; this is a data property, not a bug. |

## Next steps

- For a new contributor: `docs/ARCHITECTURE.md` for the layered pipeline and component diagram; `docs/CONFIGURATION.md` for environment variables, Brutus build flags, and pipeline stage configuration; the framework specs at `pinn_instruction/markdown_conversion/framework-specs/` for the authoritative methodology.
- For running the v2.0 CTL-PINN training slice (trainex track): the Stage-0 training operator runbook `docs/runbooks/training/2026-07-18-stage0-training-operator-runbook.md`, and `.planning/ROADMAP.md` for the v2.0 phase plan. The rebuilt training code lives under `pinn/` (`train.py`, `network.py`, `evaluate.py`, `loss_catalog.py`).
- For a fresh workstation migration: `docs/runbooks/migration/exact-state-mac-migration.md` is the canonical runbook. Do not improvise — the runbook includes exact-state verification gates (B4, B5) that detect restore drift before it can pollute later work.
- For dataset conventions and the `Result:` footer parsing rules: `simulation_data/Documentation/README.md` and `.claude/rules/dataset-reference.md`.
- For development workflow: `AGENTS.md` (governance, STOP protocol, branch awareness, commit policy) and `docs/git-guidelines.md` (the `scripts/agent-commit` workflow and the `GIT_AGENT_OWNED_PATHS` rule).
- For verification tooling: `tools/spec-render-check/` (framework-spec render detector suite, added in v1.4 Phase 22).
