---
phase: 57-corrected-re-run-the-preserved-evaluation
plan: "02"
subsystem: training
tags: [causal-loss, collocation, r-ref, microbatch, diagnostics, run-04]

requires:
  - phase: 57-corrected-re-run-the-preserved-evaluation
    provides: "57-01's RED contracts for amended allocation, normalized causal loss, and observable diagnostics"
  - phase: 56-contract-amendment-train-free-gate
    provides: "The amended §3.2 recipe and governed r_ref artifact"
provides:
  - "Exact 4096-row, 16-bin collocation allocation for full and replay-only batches"
  - "Complete-batch causal physics loss with frozen R_ref normalization and differentiable bin aggregation"
  - "Raw and normalized causal telemetry with allocation counts and R_ref provenance in step logs and TensorBoard"
affects: [57-03, RUN-04]

actuals:
  tokens: 13329
  tasks: 3
  commits: 3

tech-stack:
  added: []
  patterns:
    - "Ratified allocation boundary: 256-slot batches emit one row per selected slot in each of 16 bins; 240-slot replay-only batches use deterministic 17/18-row quotas."
    - "Single computation telemetry: raw bin means, normalized means, weights, counts, and R_ref are captured from the same complete-batch controller reduction."
    - "Fail-closed conformance: ratified slot/cardinality requests refuse unsupported reductions instead of silently falling back to a smaller sample."

key-files:
  created: []
  modified:
    - pinn/data/types.py
    - pinn/data/batches.py
    - pinn/loss_catalog.py
    - pinn/training/controllers.py
    - pinn/training/step_log.py
    - pinn/training/tb_sink.py
    - pinn/conformance/census.py
    - tests/phase40/test_optimizer_phase.py

key-decisions:
  - "The amended path consumes FixedBatch.collocation_points as its physics source, aggregates all 4096 rows into 16 differentiable bin means, and invokes causal_physics_loss once per logical batch."
  - "One validated finite positive R_ref is frozen at controller construction and normalizes both the exclusive-prefix exponent and outer weighted residual reduction; omitting it preserves legacy callers through identity normalization."
  - "Energy and angular-momentum terms reuse the same collocation points; causal weights remain detached while residual gradients reach every selected row."
  - "Diagnostics publish both raw and normalized residual families plus R_ref, n_collocation_rows, and n_bins without changing existing compatible fields."

patterns-established:
  - "Bin means use differentiable index-add aggregation over the complete logical batch, so microbatch accumulation preserves counts, loss, and gradients."
  - "Telemetry sinks retain normalized residual-bin fields while exposing raw residual bins through explicit, stable names and TensorBoard panels."

requirements-completed: [RUN-04]

coverage:
  - id: D1
    description: "Production collocation allocation emits the ratified full and replay-only 4096-row, 16-bin distributions with deterministic slot provenance and fail-closed cardinality."
    requirement: RUN-04
    verification:
      - kind: unit
        ref: "python -m unittest tests.phase57.test_recipe_production_path.AllocationContractTests tests.phase39.test_batches.CollocationQuotaTests tests.phase39.test_batches.FullBatchContract -v"
        status: pass
    human_judgment: false
  - id: D2
    description: "RunController computes complete-batch normalized causal loss with gradients from every selected slot and reuses the physics set for energy/angular-momentum terms."
    requirement: RUN-04
    verification:
      - kind: unit
        ref: "python -m unittest tests.phase57.test_recipe_production_path.ProductionPathContractTests tests.phase57.test_recipe_production_path.LossNormalizationTests tests.phase50.test_causal_telemetry.CausalTelemetryOwnershipTests -v"
        status: pass
    human_judgment: false
  - id: D3
    description: "Step-log and TensorBoard sinks expose raw and normalized causal diagnostics with R_ref and exact allocation metadata."
    requirement: RUN-04
    verification:
      - kind: unit
        ref: "python -m unittest tests.phase57.test_recipe_production_path.ProductionPathContractTests -v"
        status: pass
    human_judgment: false

duration: 32 min
completed: 2026-09-08
status: complete
---

# Phase 57 Plan 02: Complete-Batch Causal Recipe Summary

**The real training path now uses the ratified 4096-row/16-bin allocation, frozen-`R_ref` normalized causal loss, and auditable raw/normalized diagnostics.**

## Performance

- **Duration:** ~32 min (from the first implementation commit at 2026-09-08T14:03:15+08:00 through the final task commit at 2026-09-08T14:34:41+08:00)
- **Started:** 2026-09-08T14:03:15+08:00
- **Completed:** 2026-09-08T14:34:41+08:00
- **Tasks:** 3/3
- **Files modified:** 8

## Accomplishments

- Implemented exact stratified collocation allocation: 256 selected slots receive 256 rows in every one of 16 bins (4096 total); replay-only 240-slot batches preserve the seeded 17/18-row multiplicity and provenance.
- Replaced the anchor-only causal path with complete-batch, differentiable 16-bin aggregation and one frozen `R_ref` used by both the causal exponent and outer physics reduction. Energy and angular momentum consume the same physics collocation set.
- Published raw and normalized bin residuals, detached weights, `R_ref`, and exact row/bin counts through the existing step-log and TensorBoard sinks.

## Task Commits

1. **Task 1: Carry one exact binned allocation from sampler to FixedBatch** — `04f23868` (`feat(57-02)`)
2. **Task 2: Replace anchor-only physics with complete normalized causal loss** — `c0259aa8` (`feat(57-02)`)
3. **Task 3: Publish raw and normalized causal diagnostics** — `a0c0955d` (`feat(57-02)`)

The task commits were already present when this summary was reconciled after an interrupted executor handoff; no implementation commit was recreated.

## Files Created/Modified

- `pinn/data/batches.py`, `pinn/data/types.py` — ratified bin-stratified allocation and provenance contract.
- `pinn/loss_catalog.py`, `pinn/training/controllers.py` — complete-batch residual aggregation, frozen `R_ref` normalization, and shared physics collocation path.
- `pinn/training/step_log.py`, `pinn/training/tb_sink.py` — raw/normalized causal telemetry and allocation metadata.
- `pinn/conformance/census.py` — updates the conformance producer shape to the amended 16-bin residual vector.
- `tests/phase40/test_optimizer_phase.py` — updates a superseded anchor-only expectation to assert the amended batch-collocation contract.

## Decisions Made

- Kept legacy callers compatible when `r_ref` is omitted by using identity normalization, while the amended controller always binds the governed artifact value.
- Preserved existing IC, angular-momentum, optimizer, and curriculum behavior outside the bounded causal/time-allocation seam.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Required correctness] Updated the conformance census residual shape**

- **Found during:** Task 2 (complete normalized causal loss)
- **Issue:** The GATE-02 census still required the pre-amendment `(2,)` residual shape, so the conformance preflight would reject the new 16-bin producer.
- **Fix:** Changed the producer check to the amended `(16,)` shape.
- **Files modified:** `pinn/conformance/census.py`
- **Verification:** Task 2 focused production-path and causal-telemetry tests passed.
- **Committed in:** `c0259aa8`

**2. [Rule 1 - Superseded contract] Updated the Phase-40 sampler-only regression**

- **Found during:** Task 2 (controller integration)
- **Issue:** One existing test asserted the anchor-only contract that Plan 57-02 explicitly supersedes.
- **Fix:** Renamed/inverted the assertion so poisoned batch collocation times fail loudly, proving the controller consumes the batch's own physics points.
- **Files modified:** `tests/phase40/test_optimizer_phase.py`
- **Verification:** The phase-40 controller regression sweep recorded in the task commit passed 170/170.
- **Committed in:** `c0259aa8`

---

**Total deviations:** 2 auto-fixed (both required compatibility/correctness repairs)
**Impact on plan:** No scientific recipe values or run behavior outside the bounded conformance seam changed.

## Issues Encountered

- The three implementation commits existed on the branch but the executor handoff had not produced `57-02-SUMMARY.md`; this summary was reconstructed from the commits and focused verification runs before advancing tracking.
- The full Phase-57 contract suite remains intentionally incomplete for later waves (17 passed, 23 failures, 6 errors) because Wave 3–4 contracts are not implemented yet. The plan-scoped allocation, production-path, normalization, and telemetry checks all pass.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Wave 3 (Plan 57-03) can proceed. The bounded production path and RUN-04 allocation/loss contract are implemented and independently covered; runtime monitor, L-BFGS freeze, checkpoint, and config work remains in Plan 57-03. No Stage-0 or held-out evaluation run was started.

---
*Phase: 57-corrected-re-run-the-preserved-evaluation*
*Completed: 2026-09-08*
