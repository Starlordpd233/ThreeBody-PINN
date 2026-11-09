---
phase: 65
phase_name: "Probe On-the-Record & Fit Harness"
project: "Three-Body Physics-Informed LLM"
generated: "2026-11-08"
counts:
  decisions: 7
  lessons: 5
  patterns: 6
  surprises: 4
missing_artifacts:
  - "65-UAT.md"
---

# Phase 65 Learnings: Probe On-the-Record & Fit Harness

Phase 65 placed the 2026-10-27 exploratory hidden-state time-signal probe on the committed record before re-running it across all seven v2.4 Phase 60 arms, and built the guarded single-orbit diagnostic fit harness (`INST-08`) with Stage-0 training-split enforcement, production evaluation/resume isolation, logger-parity proof, and a 20-step real MPS smoke fit. Under the pre-registered formatter-cell rule, the seven-arm probe reproduction matched 144 of 144 required historical fields (`0` not reproduced, `0` provenance limitations, verdict `retained`), and the 20-step smoke fit on `hierarchical/gold/1632` completed 20/20 finite updates (`0.014265 s/step`) with zero validation or test-split opens. Extracted from `65-01..06-PLAN.md`, `65-01..06-SUMMARY.md`, `65-PROBE-PREDICTION.md`, `65-PROBE-RESULT.md`, `65-SMOKE-PREDICTION.md`, `65-FINDINGS.md`, `65-CLOSEOUT.md`, `65-VERIFICATION.md`, and `STATE.md`. No UAT file exists for this phase.

## Decisions

### Preserve the 2026-10-27 exploratory scripts and tool transcripts byte-exact before any rerun
Both original scratchpad scripts (`probe_time_signal.py` and `probe_siren_init.py`, recovered from the durable file-history store after macOS `/tmp` cleanup) and the verbatim text of the two historical tool outputs (`toolu_01PUFNWxrDDsVrU8DTCH4tX3`, `toolu_01NHGWRv6pEQCJmqeAXxqonK`) are committed under `evidence/original/` with SHA-256 provenance in `source-manifest.json`, and the historical scripts are never imported or executed.

**Rationale:** `DIAG-09` requires separating what was already observed on 2026-10-27 from any new measurement before re-running the probe through governed code.
**Source:** 65-04-SUMMARY.md, 65-VERIFICATION.md, STATE.md (Decisions from 65-04)

### Define probe reproduction as exact formatter-cell inclusion with an immutable reading rule
Every historical numeric token (`.2f`, `.3f`, `.4f`, `.3g`) is mapped before the run to its exact IEEE-754 double interval (first/last representable doubles, boundary inclusion, and excluded `nextafter` neighbors). All 144 required fields reproducing keeps the association (`retained`); any required mismatch withdraws the lead (`withdrawn`); single-arm moving/spike/skip-siren columns are `preserved_only`; and deep-layer values for the other six arms are `new_measurement` entries.

**Rationale:** formatter-defined rounding cells prevent post-hoc tolerance widening while respecting exact round-half-even ties, signed zero, and `.3g` trailing-zero rules.
**Source:** 65-04-SUMMARY.md, 65-PROBE-PREDICTION.md, 65-PROBE-RESULT.md

### Share one centred-neighbour similarity implementation (`measure_time_signal`) across probe and fit harness
`pinn/verification/diagnostic_similarity.py` implements feature-wise centring across time samples, cosine similarity of successive centred rows, first-layer frequency `|w[:,0]|·omega_0/π`, output movement as the centred norm ratio, and the labelled network-autograd vs gold-finite-difference tau-rate comparator, with forward hooks removed inside `try/finally`.

**Rationale:** `INST-08(c)` requires the fit harness to log adjacent-time similarity through the exact same calculation as the `DIAG-09` probe, verified by the committed `logger-parity.json` receipt.
**Source:** 65-01-SUMMARY.md, 65-05-SUMMARY.md, STATE.md (Decisions from 65-01, 65-05)

### Restrict diagnostic data access to Stage-0 training orbits and a hash-pinned recorded normalizer
`Stage0TrainingReader` and `require_stage0_training` in `pinn/verification/diagnostic_data.py` check that the target orbit belongs to `train` and has manifest group `base_stage == 0` before any path resolution or file read, and `load_recorded_stats` reconstructs input normalization strictly from the SHA-256-pinned Phase 59 `reader_acceptance.json` (`77526e53…`) without calling `open_real_context` or touching Stage-1 or held-out data.

**Rationale:** generation-7 checkpoints included 16 Stage-1 monitor trajectories outside v2.5's Stage-0 read authority; pinning the recorded normalizer avoids opening any out-of-scope record.
**Source:** 65-02-SUMMARY.md, STATE.md (Decisions from 65-02)

### Enforce diagnostic checkpoint refusal at both CLI entry points and payload deserialization
Every tensor payload written by `diagnostic_fit.py` carries the intrinsic `inst08-diagnostic` marker. `pinn/evaluate.py` calls `require_not_diagnostic` before config/manifest load or claim creation, `pinn/train.py` calls `require_resume_not_diagnostic` before `run_dir.mkdir`, and `checkpoint.py` raises `DiagnosticCheckpointRefused` (a `NoValidCheckpointError` subclass) across `load_latest`, `fallback_scan`, `load_checkpoint`, and `load_resume_target`.

**Rationale:** defense in depth guarantees that a diagnostic fit artifact can never consume the one-time held-out evaluation or seed a production curriculum resume, even under `--resume latest`.
**Source:** 65-03-SUMMARY.md, STATE.md (Decisions from 65-03)

### Verify historical probe and smoke results against run-commit dependency bytes, not live HEAD bytes
`verify-result` checks the five/seven code dependency hashes recorded in a registration against the git tree at the recorded `run_commit` (verified as an ancestor of `HEAD`), while `check-registration` for a new launch requires live working-tree byte identity.

**Rationale:** subsequent plans legitimately edit `diagnostic_fit.py` or `diagnostic_guard.py`; binding result verification to the run commit keeps committed evidence permanently verifiable while blocking un-re-registered launches against modified code.
**Source:** 65-04-SUMMARY.md, 65-06-SUMMARY.md, 65-CLOSEOUT.md

### Accept historical probe renderer/summary quirks with explicit reuse conditions rather than mutating pinned evidence
Under owner delegation at closeout (`65-CLOSEOUT.md`), the probe registration (`f469e003`) and result (`7a943da5`) remain immutable historical evidence; the post-publish `_render_stdout` `KeyError` on `preserved_only` rows, top-level placement of `new_measurements`, missing standalone `logger-parity` CLI subcommand, and `WR-01` nested-dict marker scan limitation are documented with explicit repair-before-reuse conditions.

**Rationale:** editing `diagnostic_probe.py` and re-running would alter historical evidence for cosmetic/CLI-surface issues when the committed JSON result and inline `logger-parity.json` receipt already satisfy `DIAG-09` and `INST-08(c)`.
**Source:** 65-05-SUMMARY.md, 65-CLOSEOUT.md, 65-VERIFICATION.md

---

## Lessons

### A receipt materialized after a run cannot be checked at the run commit itself
In Plan 65-06, the first smoke admission check demanded that `logger-parity.json` exist with matching bytes at the probe's `run_commit` (`22cee7d2`), but `logger-parity.json` was materialized in the post-run commit (`484ea30c`) from the run's output. The check refused before any claim and was fixed (`b1dcacc4`) to verify the receipt at its introducing commit while requiring the probe `run_commit` to be an ancestor.

**Context:** pre-run admission gate for the 20-step MPS smoke fit in Plan 65-06.
**Source:** 65-06-SUMMARY.md, STATE.md (Decisions from 65-06)

### Stdout rendering after artifact publication can crash on secondary verdict branches if only primary branches were unit-tested
In Plan 65-05, `diagnostic_probe.py` published the complete `reproduction.json` and `logger-parity.json`, then crashed in `_render_stdout` with `KeyError: 'measured'` when formatting `preserved_only` rows (which intentionally omit `measured`). `reproduction.stdout.txt` was regenerated read-only from the committed JSON bytes with a provenance header.

**Context:** executing the single-look seven-arm probe reproduction in Plan 65-05.
**Source:** 65-05-SUMMARY.md, 65-CLOSEOUT.md

### Two-Kepler Newton solver non-convergence on synthetic fixtures must be caught narrowly as a non-applicable comparator row
On the tiny synthetic fixture orbit used in `tests/phase65`, the frozen `two_kepler_prediction` Newton solver raises `RuntimeError("solver_did_not_converge")`. Catching that specific runtime error around the comparator call and recording `failure: solver_did_not_converge` preserves synthetic testability without masking real harness errors.

**Context:** building the dataset-free synthetic fit harness in Plan 65-01.
**Source:** 65-01-SUMMARY.md, STATE.md (Decisions from 65-01)

### Gold records carry `StageLabel.UNASSIGNED` on their own record while their physical group carries `base_stage == 0`
In the admitted corpus schema, gold trajectories have `record.stage == UNASSIGNED` by design (so gold records never inflate numeric stage counts), while their Stage-0 membership lives on the physical group signature's `base_stage`. `Stage0TrainingReader` checks the group signature's `base_stage == 0` and records both fields.

**Context:** implementing `require_stage0_training` for `hierarchical/gold/1632`, `851`, and `4658` in Plan 65-02.
**Source:** 65-02-SUMMARY.md, STATE.md (Decisions from 65-02)

### `resume latest` must refuse if the newest checkpoint is diagnostic rather than falling back to an older production checkpoint
If a directory contains an older valid production checkpoint and a newer `inst08-diagnostic` checkpoint, allowing `fallback_scan` or `load_latest` to skip the diagnostic file would silently resume an older state. Raising `DiagnosticCheckpointRefused` outside the corrupt-file handler ensures `latest` fails closed.

**Context:** wiring diagnostic isolation into `pinn/training/checkpoint.py` and `pinn/train.py` in Plan 65-03.
**Source:** 65-03-SUMMARY.md, STATE.md (Decisions from 65-03)

---

## Patterns

### Formatter-cell interval pre-registration (`nextafter`-bounded IEEE-754 cells)
Convert every printed historical decimal token under its exact printf/Python format specification (`.2f`, `.3f`, `.4f`, `.3g`) into the closed hex-float interval `[min_double, max_double]` that formats to that string, and assert that `nextafter(min_double, -inf)` and `nextafter(max_double, +inf)` format to different strings.

**When to use:** reproducing historical floating-point outputs whose original raw binary values were not saved.
**Source:** 65-04-PLAN.md, 65-04-SUMMARY.md

### Scoped git tracked-and-clean registration admission
Scope `require_committed_registration` to check `git ls-files --error-unmatch` and `git status --porcelain` only on the registration file and its enumerated code/artifact dependencies, rather than requiring the entire repository working tree to be clean.

**When to use:** pre-run admission gates in worktrees that may carry unrelated user config edits or untracked scratch files.
**Source:** 65-04-SUMMARY.md, STATE.md (Decisions from 65-04)

### All-or-nothing multi-key Stage-0 pre-validation before first file open
Validate the entire requested key set (`train`, `score`, `beside`) against the committed split allowlist and Stage-0 group manifest before resolving any path or opening any HDF5 file, so a single invalid ancillary key aborts with `open_count == 0`.

**When to use:** guarded data loaders that load target and comparison trajectories together.
**Source:** 65-02-SUMMARY.md

### Optimizer construction and step interlock for read-only probes
Wrap read-only probe execution in a context manager that patches `torch.optim.Optimizer.__init__` and `step` to increment an attempt counter and raise immediately, and compare pre- and post-run SHA-256 digests of all 15 model parameter tensors.

**When to use:** proving that a diagnostic probe on trained weights performed zero gradient updates.
**Source:** 65-04-SUMMARY.md, 65-05-SUMMARY.md

### Synchronized per-segment MPS timing (`torch.mps.synchronize`)
Bracket warmup steps, measured update steps, similarity logging, frozen scoring, data loading, and publication I/O with `torch.mps.synchronize()` (when running on MPS) and record `sync_overhead_seconds` and `sync_calls` alongside `seconds_per_step`.

**When to use:** benchmarking step throughput on asynchronous GPU/MPS backends during short smoke or timing runs.
**Source:** 65-06-SUMMARY.md

### Subclassing domain exceptions (`DiagnosticCheckpointRefused(NoValidCheckpointError)`) for backward-compatible refusal
Make the new security/isolation exception inherit from the existing caller-expected exception class while checking the new marker before structural schema validation.

**When to use:** adding a new refusal reason across existing callers and CLI entry points without breaking legacy exception-handling contracts.
**Source:** 65-03-SUMMARY.md

---

## Surprises

### All 144 required historical time-signal fields reproduced to the exact printed digit across all seven v2.4 arms
Despite re-implementing the probe cleanly in `pinn/verification/diagnostic_similarity.py` and `diagnostic_probe.py`, every single one of the 144 required historical cells across `r1-1632`, `r1-851`, `r1-4658`, and `g2s-1632-w060..w480` landed inside its exact formatter-defined rounding cell on the first and only run (`0` not reproduced).

**Impact:** confirmed the 2026-10-27 exploratory observation (`retained`) as a solid on-the-record baseline without triggering a `SCOPE-49` withdrawal pivot.
**Source:** 65-05-SUMMARY.md, 65-PROBE-RESULT.md

### The original 2026-10-27 `/tmp` scratchpad scripts had been wiped by macOS cleanup and were recovered byte-exact from local file-history snapshots
When Phase 65 began, `/tmp/probe_time_signal.py` and `/tmp/probe_siren_init.py` were no longer in `/tmp`; the orchestrator recovered the exact snapshots (`85ac6b7d6b97691b@v2` and `4f2e7a23e12db4e1@v2`) from the local file-history store and verified their SHA-256 digests before committing them under `evidence/original/`.

**Impact:** preserved complete byte-for-byte provenance for `DIAG-09` without relying on memory or reconstruction.
**Source:** 65-04-SUMMARY.md, STATE.md (Decisions from 65-04)

### By layer `h6`, adjacent-time hidden activations in every v2.4 trained network have cosine similarity `1.000000`
The new per-layer measurements (`130` raw entries across `h1..h12`) showed that while the input layer and `h1` retain time variation (`cos ≈ 0.996..0.9999`), progressive attenuation through the 12 residual SIREN blocks collapses adjacent-time cosine similarity to `1.0000` (to six decimal places) from `h6` through `h12` on every Phase 60 arm.

**Impact:** directly motivated Phase 66 (`EXP-01`, 1-hidden-layer control with `first_omega_0 = 1000`) and Phase 67 (`EXP-02` depth ladder).
**Source:** 65-PROBE-RESULT.md, 65-05-SUMMARY.md

### In a 20-step smoke fit, fixed scoring and logging overhead exceeds the 18 measured MPS update steps by 7x
In the Plan 65-06 smoke run on `hierarchical/gold/1632`, the 18 measured MPS update steps took only `0.25678 s` (`0.014265 s/step`), whereas frozen FEAS-01 scoring (`1.21599 s`), similarity logging (`0.57212 s`), setup (`0.52892 s`), and data load (`0.25356 s`) brought total wall time to `2.719 s` (`0.13597 s` per completed step).

**Impact:** drove Phase 66 and Phase 67 budget calculators to model fixed launch/scoring/logging overhead separately from marginal per-step update time.
**Source:** 65-06-SUMMARY.md, 65-FINDINGS.md
