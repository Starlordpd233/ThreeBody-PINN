---
phase: 43-verification-stage-0-pilot-acceptance
plan: 01
subsystem: testing
tags: [verification, cli, unittest, atomic-io, fingerprint, fail-closed, mps, autograd]

# Dependency graph
requires:
  - phase: 37-runtime-and-ad-verification
    provides: "pinn.runtime.resolve_runtime (the explicit precision/device seam) and componentwise_ad.run_probe_arm"
  - phase: 38-probe-suite
    provides: "run_gradcheck, run_residual_on_ground_truth, run_overfit and the canonical read-only Brutus fixture"
  - phase: 41-config-checkpointing-resume-determinism
    provides: "pinn.training.atomic_io.atomic_write_text and the pinn/train.py CLI composition-root convention"
  - phase: 42-operator-runbook-and-monitoring
    provides: "tests/phase42 subprocess launch helpers and the pinn-train interpreter path"
provides:
  - "python -m pinn.verify — the ordered five-rung ACC-01 pre-flight ladder"
  - "runs/.verify/latest-marker.json — the atomic verdict marker with a runtime+code fingerprint"
  - "marker_is_green_and_fresh — the fail-closed predicate the >30-min launch gate consumes"
  - "tests/phase43 — the Phase-43 unittest scaffold (skip phrase + re-exported subprocess helpers)"
affects: [43-04 launch duration gate, 43-06 smoke run, 43-07 pilot, 43-08 verdict]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Ladder orchestration by in-process library call, never subprocess (CTX-70)"
    - "Per-rung exception capture: a raised rung, an unimportable module, and a missing symbol are all that rung's FAIL"
    - "Runtime+code fingerprint marker gating a long-running operation"

key-files:
  created:
    - pinn/verify.py
    - tests/phase43/__init__.py
    - tests/phase43/_fixtures.py
    - tests/phase43/test_verify_ladder.py
  modified: []

key-decisions:
  - "Marker freshness window set to 24 h (DEFAULT_MAX_MARKER_AGE_S), with the full fingerprint as the primary control and the window as a secondary one — CTX-71 delegates the window to plan/execution discretion"
  - "Marker lives at runs/.verify/latest-marker.json — under the already-gitignored runs/ root, resolved and refused on traversal"
  - "verify exposes --precision/--device (default float32/mps, the D1-p production arm) so the marker's device/dtype fingerprint is explicit and the ladder is testable on the fp64-CPU arm without hardware"
  - "All five rungs always run; the verdict names the FIRST failure rather than short-circuiting, so one invocation reports the whole environment"
  - "marker_is_green_and_fresh returns a plain bool — the caller in 43-04 reports its own refusal message; no second explain-API was invented"

patterns-established:
  - "Pattern: _load_probe(module, symbol) raises on an absent module or symbol so a broken probe surfaces as a rung FAIL, never a silent skip"
  - "Pattern: write the verdict marker for BOTH outcomes; the freshness predicate, not the writer, decides authority"
  - "Pattern: bounded subprocess for git identity with an explicit unavailable sentinel rather than an abort"

requirements-completed: [ACC-01]

coverage:
  - id: D1
    description: "python -m pinn.verify runs the five rungs in SPEC order (device sanity, componentwise AD, fp64-CPU gradcheck, residual-on-ground-truth, single-trajectory overfit) as in-process library calls and exits 0 only when all pass"
    requirement: ACC-01
    verification:
      - kind: unit
        ref: "tests/phase43/test_verify_ladder.py#LadderOrderTests.test_ladder_order_is_the_spec_order"
        status: pass
      - kind: unit
        ref: "tests/phase43/test_verify_ladder.py#AllPassTests.test_all_four_probes_are_invoked_as_library_calls"
        status: pass
      - kind: unit
        ref: "tests/phase43/test_verify_ladder.py#CliTests.test_green_ladder_exits_zero_and_prints_each_rung"
        status: pass
      - kind: other
        ref: "~/miniforge3/envs/pinn-train/bin/python -m pinn.verify --overfit-max-steps 5 --runs-root <tmp> (live: rungs 1-4 PASS on the real env + corpus)"
        status: pass
    human_judgment: false
  - id: D2
    description: "A broken or missing probe cannot silently pass: a raised rung, an unimportable probe module, and a deleted probe symbol each become that rung's FAIL, and the non-zero exit names the FIRST failed rung (SPEC edge R1)"
    requirement: ACC-01
    verification:
      - kind: unit
        ref: "tests/phase43/test_verify_ladder.py#RaisedRungTests.test_raised_middle_rung_fails_only_that_rung"
        status: pass
      - kind: unit
        ref: "tests/phase43/test_verify_ladder.py#MissingProbeSymbolTests.test_missing_overfit_symbol_fails_its_rung"
        status: pass
      - kind: unit
        ref: "tests/phase43/test_verify_ladder.py#MissingProbeSymbolTests.test_unimportable_probe_module_fails_its_rung"
        status: pass
      - kind: unit
        ref: "tests/phase43/test_verify_ladder.py#CliTests.test_red_ladder_exits_nonzero_naming_first_failed_rung"
        status: pass
    human_judgment: false
  - id: D3
    description: "Every ladder outcome atomically writes runs/.verify/latest-marker.json carrying a UTC timestamp, the ordered rungs, and the device/dtype/torch/python/git fingerprint; the write stays rooted under runs/ and leaves no temp file"
    requirement: ACC-01
    verification:
      - kind: unit
        ref: "tests/phase43/test_verify_ladder.py#MarkerWriteTests.test_green_outcome_writes_a_green_marker"
        status: pass
      - kind: unit
        ref: "tests/phase43/test_verify_ladder.py#MarkerWriteTests.test_red_outcome_also_writes_a_marker"
        status: pass
      - kind: unit
        ref: "tests/phase43/test_verify_ladder.py#MarkerWriteTests.test_write_is_atomic_and_leaves_no_temp_file"
        status: pass
      - kind: unit
        ref: "tests/phase43/test_verify_ladder.py#MarkerWriteTests.test_marker_path_is_rooted_under_runs"
        status: pass
    human_judgment: false
  - id: D4
    description: "marker_is_green_and_fresh is fail-closed on every axis — red verdict, stale/future/malformed timestamp, device/dtype/torch/python mismatch, differing Git head, and a git-unavailable marker are each refused"
    requirement: ACC-01
    verification:
      - kind: unit
        ref: "tests/phase43/test_verify_ladder.py#MarkerFreshnessTests.test_stale_marker_is_rejected"
        status: pass
      - kind: unit
        ref: "tests/phase43/test_verify_ladder.py#MarkerFreshnessTests.test_runtime_mismatch_is_rejected"
        status: pass
      - kind: unit
        ref: "tests/phase43/test_verify_ladder.py#MarkerFreshnessTests.test_code_mismatch_is_rejected"
        status: pass
      - kind: unit
        ref: "tests/phase43/test_verify_ladder.py#MarkerFreshnessTests.test_git_unavailable_marker_cannot_authorize_a_long_run"
        status: pass
    human_judgment: false
  - id: D5
    description: "A failing git rev-parse HEAD (OSError, timeout, non-zero exit) degrades the marker to git_head_available false rather than aborting verify"
    requirement: ACC-01
    verification:
      - kind: unit
        ref: "tests/phase43/test_verify_ladder.py#GitHeadFallbackTests.test_oserror_reports_unavailable"
        status: pass
      - kind: unit
        ref: "tests/phase43/test_verify_ladder.py#GitHeadFallbackTests.test_verify_still_reports_its_ladder_when_git_is_unavailable"
        status: pass
    human_judgment: false
  - id: D6
    description: "tests/phase43 scaffold: the established deferred-import skip phrase plus re-exported Phase-42 subprocess helpers and the pinn-train interpreter path, dataset-free and I/O-free at import"
    verification:
      - kind: other
        ref: "~/miniforge3/envs/pinn-train/bin/python -c \"import tests.phase43, tests.phase43._fixtures\""
        status: pass
    human_judgment: false
  - id: D7
    description: "SPEC prohibition backstop: pinn/verify.py only orchestrates the four pre-existing probes — no new physics probe, and no model/loss/data/training-loop change"
    verification: []
    human_judgment: true
    rationale: "Scope compliance is a diff-review judgment (SPEC verification tier: judgment). The tests assert library-call orchestration, but only a human reading the diff can confirm no prohibited surface was touched."

# Metrics
duration: 30 min
completed: 2026-07-21
status: complete
---

# Phase 43 Plan 01: Verify Ladder & Fresh-Marker Fingerprint Summary

**`python -m pinn.verify` — an ordered five-rung pre-flight that orchestrates the four existing probes as in-process library calls, names its first failure, and writes an atomic `runs/.verify/latest-marker.json` fingerprinted by device, dtype, Torch, Python and Git head so only a fresh green marker from the same code can authorize a long run.**

## Performance

- **Duration:** ~30 min
- **Started:** 2026-07-20T22:44Z (local 2026-07-20 22:44 PDT)
- **Completed:** 2026-07-21T06:13Z (commit `9aeccce`)
- **Tasks:** 3
- **Files modified:** 4 created, 0 modified

## Accomplishments

- **ACC-01 ladder is executable.** `pinn/verify.py` runs device sanity → componentwise AD → fp64-CPU gradcheck → residual-on-ground-truth → single-trajectory overfit, prints per-rung PASS/FAIL plus one overall verdict, and returns 0 only when every rung passed.
- **A broken probe cannot silently pass.** `_load_probe` raises on an unimportable module or an absent symbol, and `_record_rung` converts any rung exception into that rung's FAIL record. All five rungs still run, so one invocation reports the whole environment, and the non-zero verdict names the FIRST failure in ladder order.
- **The AD rung's verdict is derived correctly.** `run_probe_arm` exposes no top-level pass flag, so the rung ANDs every pattern's own `passed` with a null `exception` — the interface trap the plan called out.
- **The long-run gate has a code-specific proof.** Every outcome (green and red) atomically writes `runs/.verify/latest-marker.json` via `atomic_write_text`, carrying a UTC timestamp, the ordered rungs, the first failed rung, and the fingerprint `{device, dtype, torch_version, python_version, git_head, git_head_available}`. `marker_is_green_and_fresh` compares all of it and refuses anything that does not match exactly.
- **Git unavailability degrades the marker, not verify.** A bounded (10 s) `git rev-parse HEAD` treats `OSError`, any `SubprocessError` including `TimeoutExpired`, a non-zero exit, and empty output as unavailable; verify still reports its ladder, and the resulting `git_head_available: false` marker can never authorize a long run.
- **Phase-43 test convention is in place.** `tests/phase43/` carries the established skip phrase and re-exports only the Phase-42 subprocess helpers plus the `pinn-train` interpreter path — dataset-free, I/O-free at import, no bespoke smoke harness.

## Task Commits

1. **Task 1: Phase-43 unittest scaffold** — `2c1ed4a` (test)
2. **Task 2: five-rung verify CLI** — `02c0cfd` (test, RED) → `c0390f9` (feat, GREEN)
3. **Task 3: complete fresh-marker fingerprint** — `d46f7c1` (test, RED) → `9aeccce` (feat, GREEN)

_TDD tasks carry a test commit then a feat commit; no refactor commit was needed._

## Files Created/Modified

- `pinn/verify.py` — the ACC-01 ladder orchestrator, marker writer/reader, and fail-closed freshness predicate (CLI: `python -m pinn.verify`).
- `tests/phase43/__init__.py` — sole definition of the `skipped Phase43 production symbol` skip phrase.
- `tests/phase43/_fixtures.py` — re-exports the Phase-42 subprocess helpers and `CONDA_PYTHON`; owns no fixture bodies.
- `tests/phase43/test_verify_ladder.py` — 41 tests over the ladder, the missing/broken-probe paths, the marker write, the Git fallback, and the freshness predicate.

## Verification Results

| Command | Result |
|---|---|
| `~/miniforge3/envs/pinn-train/bin/python -c "import tests.phase43, tests.phase43._fixtures"` | PASS (exit 0, no output) |
| `~/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase43.test_verify_ladder -v` | PASS — Ran 41 tests, OK |
| `~/miniforge3/envs/pinn-train/bin/python -m pinn.verify --help` | PASS (usage printed, exit 0) |
| `~/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase41.test_prohibitions` (regression) | PASS — Ran 5 tests, OK |

**Live ladder evidence** (`python -m pinn.verify --overfit-max-steps 5 --runs-root <tmp>`): rungs 1–4 PASS against the real environment and the real corpus; rung 5 reports `cap_without_target`, which is the artificial 5-step cap (the probe's own gate needs up to 3000 steps), and the marker correctly records `verdict: red` naming `overfit_single_trajectory`. Fingerprint recorded: `mps / torch.float32 / 2.12.1 / 3.11.15 / git_head_available: true`.

Incidental finding for downstream plans: the residual and overfit rungs resolved the read-only Brutus fixture (`standard_quasi_random_gold_standard/0000`) **from inside the trainex worktree with no config and no copy**, which empirically supports RESEARCH finding #4 and the review's MEDIUM data-reachability concern for probe-side access. That is evidence about the probes' fixture loader, not about `AdmittedSetAdapter`'s Stage-0 admitted set — plan 43-03 must still confirm its own path.

## Decisions Made

- **Freshness window = 24 h.** CTX-71 and CONTEXT "Claude's Discretion" explicitly delegate the marker path and freshness window to plan/execution. The full runtime+code fingerprint is the primary control (any code or runtime change invalidates the marker immediately); the window is a secondary guard against an unattended machine-level change riding along. Exposed as `DEFAULT_MAX_MARKER_AGE_S` and as a `max_age_s` parameter so 43-04 can tighten it without editing this module.
- **Marker path = `runs/.verify/latest-marker.json`.** Under the already-gitignored `runs/` root (SPEC: marker writes rooted under `runs/`), resolved with a traversal refusal mirroring `pinn/train.py::_resolve_run_dir`.
- **`--precision` / `--device` flags, defaulting to the D1-p production arm (float32/mps).** Every probe CLI already requires an explicit pair, `resolve_runtime` mandates one, and the marker fingerprint must record which pair was certified. The flags also let the ladder tests exercise the fp64-CPU arm without hardware.
- **All five rungs always run.** Short-circuiting on the first failure would hide the rest of the environment from the operator; the verdict still names the first failure, which is what SPEC AC 2 requires.
- **`marker_is_green_and_fresh` returns a plain `bool`.** No parallel "explain why" API was invented; plan 43-04 owns its own refusal message.
- **The freshness predicate refuses a git-unavailable marker on both sides.** If either the marker or the current fingerprint lacks Git availability, the marker is refused — the plan's behavior clause states such a marker "cannot authorize a long run", and a marker whose code identity is unknown cannot be matched against current code.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Interleaved stdout/stderr hid the ladder under the verdict**
- **Found during:** Task 3 (live ladder run)
- **Issue:** The red verdict goes to stderr (matching `pinn/train.py`'s error idiom) while the per-rung lines go to stdout; unflushed stdout made a terminal print the verdict line *above* the ladder it summarizes.
- **Fix:** `sys.stdout.flush()` before the stderr verdict print.
- **Files modified:** `pinn/verify.py`
- **Verification:** 41/41 tests still pass; the live run now prints the ladder first.
- **Committed in:** `9aeccce` (Task 3 commit)

**2. [Rule 1 - Bug] Marker-path test compared an unresolved macOS temp path**
- **Found during:** Task 3 (GREEN)
- **Issue:** `marker_path` resolves both sides, so on macOS the returned path is `/private/var/...` while the test's expectation was the unresolved `/var/...` symlink — a test defect, not an implementation one.
- **Fix:** Resolve the expectation in the test and comment why.
- **Files modified:** `tests/phase43/test_verify_ladder.py`
- **Verification:** `test_marker_path_is_rooted_under_runs` passes; the containment assertion is unchanged.
- **Committed in:** `9aeccce` (Task 3 commit)

### Process deviation (no code impact)

**3. [Process] Task 3's implementation was written before its RED test, then withdrawn to restore the gate**
- **Found during:** Task 2 → Task 3 boundary
- **Issue:** `pinn/verify.py` was first authored in a single pass containing both Task 2's ladder and Task 3's marker surface, which would have made Task 3's RED gate vacuous (its tests would have passed on arrival).
- **Fix:** The marker block was removed from the Task 2 commit (`c0390f9` contains the ladder only), Task 3's tests were written and observed failing (31 of 41 ERRORing on the absent marker symbols, `d46f7c1`), and only then was the marker implementation restored (`9aeccce`). Both TDD gates are therefore genuine and visible in git history.
- **Files modified:** none beyond the plan's owned files.
- **Verification:** `git log` shows `test → feat` ordering for both Task 2 and Task 3.

---

**Total deviations:** 2 auto-fixed (2 bugs) + 1 process correction
**Impact on plan:** No scope change. Both auto-fixes are local to this plan's own files; the process correction restored the plan's mandated TDD gate rather than papering over it.

## Issues Encountered

- **Rung 5 does not pass under an artificial step cap.** The live run used `--overfit-max-steps 5` to stay bounded; the overfit probe's own gate needs up to 3000 steps to reach its ≥1e3× loss-drop criterion, so it honestly reported `cap_without_target`. This is the probe's certified behavior, not a ladder defect. A full unbounded green-ladder run is left to the operator/43-06, where the runtime cost is budgeted.

## Known Stubs

None. Every symbol this plan ships is wired and exercised by a test; nothing returns a placeholder value.

## Threat Flags

None. No new network endpoint, auth path, or schema at a trust boundary was introduced. The plan's own register (T-43-01-01 tampering, T-43-01-02 repudiation) is mitigated as planned: the marker write is atomic and runs-rooted with a complete fingerprint and a fail-closed Git fallback, and every rung failure is caught and recorded rather than skipped.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- **Ready for 43-04.** `read_verify_marker(runs_root)`, `current_fingerprint(precision=, device=)`, and `marker_is_green_and_fresh(marker, fingerprint=, now=, max_age_s=)` are the stable surface the >30-min launch gate consumes. `DEFAULT_MAX_MARKER_AGE_S` is overridable per call.
- **Ready for 43-02/43-05/43-06/43-07.** `tests/phase43/__init__.py::_SKIP_PHRASE` and `tests/phase43/_fixtures.py` are the shared convention; the subprocess launch helpers are already re-exported.
- **Open for the operator.** No unbounded green-ladder run has been performed; the >30-min gate has no green marker to read until one is. 43-06's smoke is the natural place to produce it.

## Self-Check: PASSED

- All four created files exist on disk (`pinn/verify.py`, `tests/phase43/{__init__,_fixtures,test_verify_ladder}.py`).
- All five task commits resolve in `git log`: `2c1ed4a`, `02c0cfd`, `c0390f9`, `d46f7c1`, `9aeccce`.
- `git diff --diff-filter=D a39abcbe..HEAD` reports no deletions — no pre-existing file was removed.
- All three plan `<verify>` commands and the plan-level `<verification>` command re-run green (41/41 tests).

---
*Phase: 43-verification-stage-0-pilot-acceptance*
*Completed: 2026-07-21*
