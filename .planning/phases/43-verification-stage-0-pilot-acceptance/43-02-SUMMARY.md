---
phase: 43-verification-stage-0-pilot-acceptance
plan: 02
subsystem: verification-acceptance
tags: [acc-03, gate-metric, hamiltonian, evaluate-cli, single-eval, weights-only]
status: complete
requires:
  - 43-03 (data.root/data.source config seam, CPU/fp32 AdmittedSetAdapter,
    runs/<run>/splits.json persistence, frozen config.yaml freeze path)
  - pinn/network.py (forward(tau_ic13, masses) -> COM-projected positions)
  - pinn/data/{adapter,splits}.py (AdmittedSetAdapter, StageIndex.from_split)
  - pinn/training/{checkpoint,atomic_io,config_yaml}.py
provides:
  - "pinn.verification.gate_metrics: no-grad finite-difference velocity + matched-Plummer float64/eps_inv=1e-10 Hamiltonian + worst-trajectory aggregation + SCS + the single gate_verdict source of truth"
  - "pinn.evaluate: python -m pinn.evaluate --checkpoint <ckpt> --output <dir>, the milestone's sole one-time held-out ACC-03 gate renderer"
  - "runs/<run>/evaluation/{metrics.json,metrics.md,evaluation-receipt.json} artifact contract"
affects:
  - 43-05 (summary.md test-set preview + gate result feed from this evaluator's output)
  - 43-08 (go/adjust/rethink verdict cites this gate result)
tech-stack:
  added: []
  patterns:
    - "no-grad finite-difference metric module (positions -> velocity via finite differences, never input-time autograd)"
    - "checkpoint-ownership resolution (checkpoints/<file>.pt -> run_dir containing frozen config.yaml + splits.json)"
    - "single-source-of-truth verdict (gate_verdict derives PASS/FAIL from eps_H alone; SCS is display-only, avoiding a two-independent-booleans render)"
    - "fail-closed single-evaluation receipt (a pre-existing evaluation-receipt.json at --output refuses any rerun)"
key-files:
  created:
    - pinn/verification/gate_metrics.py
    - pinn/evaluate.py
    - tests/phase43/test_gate_boundary.py
    - tests/phase43/test_evaluate_gate.py
    - tests/phase43/test_evaluate_edge_cases.py
  modified: []
key-decisions:
  - "Velocity for the gate Hamiltonian is derived by finite-differencing the model's PREDICTED positions over the persisted monotone snapshot times (one-sided endpoint + centered interior, mirroring AdmittedSetAdapter.acceleration_magnitudes) rather than input-time autograd — the model forward pass stays a single torch.no_grad() call, resolving the review HIGH concern (43-REVIEWS.md) about a no-grad/autograd conflict."
  - "gate_verdict is the SOLE PASS/FAIL source, computed from the aggregate eps_H only; SCS is a derived display quantity (scs_from_eps_h), never an independent second verdict check — avoids the 'two independently-driftable booleans' anti-pattern the cross-AI review praised avoiding."
  - "The evaluation-receipt.json rerun-refusal is scoped to the operator-supplied --output directory (not a hidden run-scoped location) — matches the plan's literal three-artifact-per-directory contract; the receipt still binds checkpoint/config/splits sha256 digests for provenance audit even though the refusal itself is unconditional on any prior receipt's presence."
  - "Confirmed via 43-SPEC.md / 43-CONTEXT.md CTX-75 (commit 5d269156) that the SCS gate wording is already corrected in the live SPEC; no owner-precondition checkpoint was needed (the 43-REVIEWS.md MEDIUM flag about stale SCS wording applies to 43-08/CTX-75 prose only, not to this plan's own text, which was already correct)."
requirements-completed: [ACC-03]
duration: ~7min (task-commit span; excludes upfront context reading)
completed: 2026-07-21
coverage:
  - id: gate-boundary
    description: "Position-only Hamiltonian gate metric: no-grad finite-difference velocity, matched-Plummer float64/eps_inv=1e-10 Hamiltonian, worst-trajectory (max) aggregation, SCS derived only from that aggregate, and gate_verdict as the single PASS/FAIL source (FAIL on nonfinite, FAIL on eps_H > 1e-5 / SCS > -5, both boundaries PASS)."
    requirement: ACC-03
    verification:
      - kind: unit
        ref: tests/phase43/test_gate_boundary.py
        status: pass
    human_judgment: false
  - id: closed-evaluate-flow
    description: "python -m pinn.evaluate resolves checkpoint ownership, loads the frozen 43-03 config.yaml + splits.json, selects StageIndex.from_split(..., 'test') without rebuilding a split, runs one no-grad forward pass over the held-out IC13/raw-mass/persisted-time metadata, and writes matching metrics.json/metrics.md/evaluation-receipt.json."
    requirement: ACC-03
    verification:
      - kind: unit
        ref: tests/phase43/test_evaluate_gate.py
        status: pass
    human_judgment: false
  - id: evaluate-fail-closed-edges
    description: "Empty test view, checkpoint-ownership refusal, --output escaping the runs root, malformed frozen inputs (config.yaml/splits.json), a nonfinite gate metric (honest FAIL artifact, no crash), and a rerun against an existing receipt (single-eval discipline) all refuse or render honestly rather than crashing or fabricating a value."
    requirement: ACC-03
    verification:
      - kind: unit
        ref: tests/phase43/test_evaluate_edge_cases.py
        status: pass
    human_judgment: false
---

# Phase 43 Plan 02: Held-Out Evaluate Gate & Hamiltonian Metric Summary

**One-time `pinn.evaluate` CLI that reconstructs the persisted held-out test split from a checkpoint's frozen run provenance and renders the authoritative post-v1.3 binary gate (worst-case Hamiltonian drift, matched-Plummer `eps_inv=1e-10`) with a single-evaluation receipt.**

## Performance

- **Duration:** ~7 min (span between the first RED commit and the final GREEN commit; excludes upfront plan/spec/context reading)
- **Tasks:** 2/2 completed
- **Files:** 2 created (production) + 3 created (tests) = 5 files, 0 modified
- **Tests:** 46/46 pass (29 gate-boundary + 7 evaluate-gate + 10 evaluate-edge-cases)

## Accomplishments

- **`pinn/verification/gate_metrics.py`** — a pure, no-grad metric module:
  - `finite_difference_velocity`: one-sided endpoint + centered interior finite differences over persisted monotone times (never input-time autograd), returning a detached CPU float64 tensor.
  - `matched_plummer_hamiltonian_series`: `H = T + V` on detached CPU float64 tensors, `T = 0.5*sum(m_i*||v_i||^2)`, `V` using the matched-Plummer potential-only softening `eps_inv = 1e-10` (never the training softening `EPS_SOFT = 1e-5`).
  - `trajectory_eps_h` / `aggregate_test_eps_h`: per-trajectory `eps_H = max_t |(H(t)-H(0))/H(0)|`, and the test-set aggregate as the WORST (maximum) finite per-trajectory value — any nonfinite trajectory makes the aggregate nonfinite (never silently dropped).
  - `scs_from_eps_h` / `gate_verdict`: `SCS = log10(eps_H)` for display; `gate_verdict` is the SOLE PASS/FAIL source (FAIL on nonfinite or `eps_H > 1e-5`, both the `eps_H == 1e-5` and the equivalent `SCS == -5` boundaries PASS).
- **`pinn/evaluate.py`** — `python -m pinn.evaluate --checkpoint <ckpt> --output <dir>`:
  - `_resolve_owning_run`: refuses a checkpoint not owned by a run with a frozen `config.yaml` + persisted `splits.json`.
  - Loads that run's exact 43-03 contract: `load_config`, `SplitManifest.from_path`, a fresh CPU/float32 `AdmittedSetAdapter`, and `StageIndex.from_split(adapter, manifest, "test")` — never `write_split_manifest` (no split rebuilt), and no train/validation argument accepted.
  - Refuses an empty test view (`EmptyTestSetError`) before any model construction.
  - Loads the model with `weights_only=True`, builds `[tau, IC13]` from each held-out record's persisted times + normalized IC13 + raw masses, and runs the ENTIRE test split through one `.eval()` + `torch.no_grad()` forward pass.
  - Writes atomic `metrics.json` / `metrics.md` (with a `## Gate Check` block, plain-English `ε_H`/SCS descriptions, and a matching `OVERALL: PASS/FAIL`) / `evaluation-receipt.json` (binding checkpoint/config/splits sha256 digests + timestamp + verdict).
  - A pre-existing receipt at `--output` refuses any rerun (`EvaluationReceiptExistsError`); `--output` is path-guarded beneath a `runs/` root (`OutputPathEscapeError`).

## Task Commits

1. **Task 1: Define the position-only Hamiltonian metric and gate**
   - `5f5331c5` — `test(43-02): add failing tests for the position-only Hamiltonian gate metric` (RED, 29 tests SKIP)
   - `d3b8410f` — `feat(43-02): implement the position-only Hamiltonian gate metric` (GREEN, 29/29 pass)
2. **Task 2: Implement closed one-time evaluate data flow**
   - `3d0c8075` — `test(43-02): add failing tests for the closed one-time evaluate data flow` (RED, 17 tests SKIP)
   - `2fc6601b` — `feat(43-02): implement the closed one-time evaluate CLI` (GREEN, 17/17 pass)

_Note: both tasks are TDD (`tdd="true"`); each landed as a RED commit (tests only, SKIP under the Phase-43 deferred-symbol convention) followed by a GREEN commit (implementation, full pass)._

## Files Created/Modified

- `pinn/verification/gate_metrics.py` — the ACC-03 position-only Hamiltonian gate metric module (new).
- `pinn/evaluate.py` — the one-time held-out `python -m pinn.evaluate` CLI (new).
- `tests/phase43/test_gate_boundary.py` — 29 tests covering finite-difference velocity, the matched-Plummer Hamiltonian, worst-trajectory aggregation, both gate-boundary equalities, above/below thresholds, and NaN/Inf FAIL.
- `tests/phase43/test_evaluate_gate.py` — 7 tests covering the closed happy-path flow: matching metrics.json/metrics.md numbers and verdict, no split rebuilt, `StageIndex.from_split(..., "test")` selection, held-out record consumption, receipt digest binding, and the CLI exit code.
- `tests/phase43/test_evaluate_edge_cases.py` — 10 tests covering empty test view, checkpoint-ownership refusal, output-path escape, malformed `config.yaml`/`splits.json`, a nonfinite gate metric rendering an honest FAIL artifact, and rerun-receipt refusal.

## Decisions Made

See `key-decisions` in the frontmatter. In brief: velocity is derived by finite-differencing predicted positions (not autograd) so the model forward pass stays a single `torch.no_grad()` call; `gate_verdict` is the sole PASS/FAIL source (SCS is display-only); the evaluation receipt lives alongside `metrics.json`/`metrics.md` at the operator-supplied `--output` (matching the plan's literal three-artifact-per-directory contract) rather than a separate hidden run-scoped location, while still binding checkpoint/config/splits digests for provenance.

## Deviations from Plan

**One test-authoring correction (not a deviation from the plan's implementation contract):**

**1. [Rule 1 - Bug, in my own test] Fixed a physically-invalid "conserved trajectory" test fixture**
- **Found during:** Task 1 GREEN verification.
- **Issue:** `ComputeTrajectoryGateMetricsTests` originally modeled one body moving at constant velocity relative to two STATIC bodies and asserted `eps_H == 0`. That trajectory is not a solution to the gravitational two/three-body problem (the pairwise separations — and therefore the potential energy — change over time even though the kinetic energy is constant), so its Hamiltonian is genuinely NOT conserved; the assertion was physically wrong, not the implementation.
- **Fix:** Replaced the fixture with a genuinely static three-body configuration (zero velocity, fixed separations at every snapshot), which IS exactly conserved by construction.
- **Files modified:** `tests/phase43/test_gate_boundary.py` (test-only; landed in the same GREEN commit `d3b8410f`, not a separate fix commit, since the RED commit had already been made and the file was still mid-flight toward GREEN).
- **Verification:** All 29 `test_gate_boundary` tests pass.

**Also, one indentation bug in my own edge-case test** (assertions reading artifacts after their `tempfile.TemporaryDirectory()` context had already closed) was caught and fixed before the GREEN commit for Task 2, landing directly in `2fc6601b`.

**Total deviations:** 0 against the PLAN's specified implementation contract. Both corrections above were bugs in this session's own test authoring, caught and fixed before the corresponding GREEN commit — no plan-level deviation, no architectural change, no scope creep.

## Known Stubs

None. `pinn/evaluate.py` implements the full closed flow end-to-end (checkpoint ownership → frozen provenance load → real adapter/split reconstruction → real model forward pass → real gate metrics → real atomic artifact writes); no placeholder data, no hardcoded empty defaults, no "coming soon" text. Plotting is explicitly out of scope per the plan (SPEC boundary: `metrics.json`/`metrics.md` never depend on it) and was not stubbed — it simply was not attempted.

## Issues Encountered

None beyond the two self-caught test bugs documented above under Deviations.

## Next Phase Readiness

- `pinn.evaluate` is ready for plan 43-08 (go/adjust/rethink verdict) to consume: its `metrics.json`/`metrics.md` output is the milestone's sole ACC-03 acceptance-gate rendering, and the `EvaluationOutcome` (`verdict`, `eps_h`, `scs`, `n_test_trajectories`) gives a stable programmatic surface.
- Plan 43-05 (`summary.md` enrichment) can read `runs/<run>/evaluation/metrics.json` for its test-set preview + gate-result feed.
- Not yet exercised against the REAL admitted Stage-0 corpus or a genuinely-trained checkpoint (this plan's tests use `tests/phase39/_fixtures.TinyCorpus` — a small synthetic on-disk corpus — plus freshly-initialized untrained model weights, per the Phase-43 dataset-free test convention). The first real invocation happens downstream once a real Stage-0 checkpoint exists (plans 43-06/43-07).
- No blockers for 43-05/43-08.

## Self-Check: PASSED

- `pinn/verification/gate_metrics.py` — FOUND
- `pinn/evaluate.py` — FOUND
- `tests/phase43/test_gate_boundary.py` — FOUND
- `tests/phase43/test_evaluate_gate.py` — FOUND
- `tests/phase43/test_evaluate_edge_cases.py` — FOUND
- Commit `5f5331c5` — FOUND
- Commit `d3b8410f` — FOUND
- Commit `3d0c8075` — FOUND
- Commit `2fc6601b` — FOUND
- Verification command `~/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase43.test_gate_boundary tests.phase43.test_evaluate_gate tests.phase43.test_evaluate_edge_cases -v` — 46/46 PASS

---
*Phase: 43-verification-stage-0-pilot-acceptance*
*Completed: 2026-07-21*
